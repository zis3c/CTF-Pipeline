"""Minimal CTFd client used in place of the upstream (unavailable) `ctfd` CLI.

The pipeline shells out to `python -m ctfd -d ROOT {init,sync,challenges}` and
expects `.ctfd/config.json` with a `CTFD` block and a `Challenges` list. This
module implements exactly that contract against the CTFd REST API.

Authentication order:
  1. `Authorization: Token <token>` using the configured/env token.
  2. Fallback to username/password login (session cookie) from
     `CTFD_USERNAME`/`CTFD_PASSWORD` (or `CTFD_USER`/`CTFD_PASS`).
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import requests

UA = "CTFd-CLI-v0.1-by-@TheFlash2k"
CONFIG_REL = Path(".ctfd") / "config.json"
CHALLENGE_FIELDS = (
    "id", "name", "category", "type", "value",
    "description", "connection_info", "files", "hints",
)


def slug(value, fallback="challenge"):
    value = re.sub(r"[^a-zA-Z0-9]+", "-", str(value)).strip("-").lower()
    return value or fallback


def category(value):
    v = str(value).lower()
    names = [
        ("cryptography", "crypto"), ("web exploitation", "web"),
        ("binary exploitation", "pwn"), ("reverse engineering", "reverse"),
        ("digital forensics", "forensics"), ("mobile exploitation", "mobile"),
        ("osint", "osint"), ("miscellaneous", "misc"),
        ("boot2root", "boot2root"), ("selamat", "welcome"),
    ]
    for needle, short in names:
        if needle in v:
            return short
    return slug(value, "other")


def config_path(root):
    return Path(root) / CONFIG_REL


def load_config(root):
    p = config_path(root)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"CTFD": {}, "Challenges": []}


def save_config(root, cfg):
    p = config_path(root)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _creds():
    for uk, pk in (("CTFD_USERNAME", "CTFD_PASSWORD"), ("CTF_USERNAME", "CTF_PASSWORD"),
                   ("CTFD_USER", "CTFD_PASS"), ("CTF_USER", "CTF_PASS")):
        user, pw = os.environ.get(uk), os.environ.get(pk)
        if user and pw:
            return user, pw
    return None, None


class CtfdClient:
    def __init__(self, base, token=None):
        self.base = str(base).rstrip("/")
        self.token = (token or "").strip()
        self.token_auth = False
        self.session_auth = False
        self.s = requests.Session()
        self.s.headers["User-Agent"] = UA

    def _login(self, user, pw):
        page = self.s.get(self.base + "/login", timeout=30)
        m = re.search(r'name="nonce"\s+type="hidden"\s+value="([^"]+)"', page.text)
        self.s.post(
            self.base + "/login",
            data={"name": user, "password": pw, "_submit": "Submit", "nonce": m.group(1) if m else ""},
            timeout=30, allow_redirects=False,
        )
        me = self.s.get(self.base + "/api/v1/users/me", timeout=30)
        self.session_auth = me.status_code == 200 and "json" in me.headers.get("content-type", "")
        return self.session_auth

    def authenticate(self):
        if self.token:
            r = self.s.get(
                self.base + "/api/v1/users/me",
                headers={"Authorization": "Token " + self.token}, timeout=30, allow_redirects=False,
            )
            if r.status_code == 200 and "json" in r.headers.get("content-type", ""):
                self.token_auth = True
                return ("token", r.json().get("data", {}).get("name", ""))
        user, pw = _creds()
        if user and pw and self._login(user, pw):
            me = self.s.get(self.base + "/api/v1/users/me", timeout=30).json().get("data", {})
            return ("session", me.get("name", ""))
        if self.token:
            raise SystemExit("CTFd rejected the token and no CTFD_USERNAME/CTFD_PASSWORD were provided.")
        raise SystemExit("No CTFd credentials. Configure a token or set CTFD_USERNAME/CTFD_PASSWORD.")

    def get(self, path, **kw):
        headers = kw.pop("headers", {})
        if self.token_auth:
            headers["Authorization"] = "Token " + self.token
        return self.s.get(self.base + path, headers=headers, timeout=30, **kw)

    def challenge_list(self):
        r = self.get("/api/v1/challenges")
        r.raise_for_status()
        return r.json().get("data", [])

    def challenge_detail(self, cid):
        r = self.get(f"/api/v1/challenges/{cid}")
        r.raise_for_status()
        return r.json().get("data", {})

    def fetch_detailed(self):
        out = []
        for item in self.challenge_list():
            d = self.challenge_detail(item["id"])
            raw_files = d.get("files") or []
            entry = {k: d.get(k) for k in CHALLENGE_FIELDS}
            # CTFd file URLs carry a per-request signed token; keep the full URL
            # for downloads but store a stable name for change detection.
            entry["file_urls"] = list(raw_files)
            entry["files"] = [str(f).split("?", 1)[0] for f in raw_files]
            out.append(entry)
        return out


def download_file(client, url, dest):
    dest = Path(dest)
    part = dest.with_name(dest.name + ".part")
    headers, mode = {}, "wb"
    if part.exists() and not dest.exists():
        headers["Range"] = f"bytes={part.stat().st_size}-"
        mode = "ab"
    r = client.s.get(url, headers=headers, timeout=120, stream=True)
    if r.status_code == 416:
        part.replace(dest)
        return dest
    if r.status_code == 200 and mode == "ab":
        mode = "wb"
    r.raise_for_status()
    with open(part, mode) as fh:
        for chunk in r.iter_content(1 << 16):
            fh.write(chunk)
    part.replace(dest)
    return dest


def cmd_init(root, args):
    url = None
    token = None
    i = 0
    while i < len(args):
        if args[i] == "--url" and i + 1 < len(args):
            url = args[i + 1]; i += 2
        elif args[i] == "--token" and i + 1 < len(args):
            token = args[i + 1]; i += 2
        else:
            i += 1
    if not url:
        raise SystemExit("init requires --url URL")
    if token is None:
        token = os.environ.get("CTFD_TOKEN") or os.environ.get("CTF_TOKEN", "")
    cfg = load_config(root)
    cfg.setdefault("CTFD", {})
    cfg["CTFD"]["URL"] = url.rstrip("/")
    cfg["CTFD"]["TOKEN"] = token
    cfg.setdefault("Challenges", [])
    save_config(root, cfg)
    print(f"Initialized profile at {config_path(root)}")


def cmd_sync(root, args):
    cfg = load_config(root)
    base = cfg.get("CTFD", {}).get("URL", "")
    if not base:
        raise SystemExit("Profile is not initialized (run `init` first)")
    client = CtfdClient(base, cfg.get("CTFD", {}).get("TOKEN"))
    mode, who = client.authenticate()
    print(f"Authenticated via {mode}: {who}")
    previous = {str(c.get("id")): c for c in cfg.get("Challenges", [])}
    detailed = client.fetch_detailed()
    for c in detailed:
        c["is_downloaded"] = bool(previous.get(str(c.get("id")), {}).get("is_downloaded", False))
    cfg["Challenges"] = detailed
    save_config(root, cfg)
    print(f"Synced {len(detailed)} challenges")


def cmd_challenges(root, args):
    cfg = load_config(root)
    base = cfg.get("CTFD", {}).get("URL", "")
    if not base:
        raise SystemExit("Profile is not initialized (run `init` first)")
    client = CtfdClient(base, cfg.get("CTFD", {}).get("TOKEN"))
    client.authenticate()
    root = Path(root)
    for chal in cfg.get("Challenges", []):
        target = root / category(chal.get("category", "Other")) / slug(chal.get("name", "challenge"))
        for sub in ("work", "notes", "flag_output_dir"):
            (target / sub).mkdir(parents=True, exist_ok=True)
        for f in (chal.get("file_urls") or chal.get("files") or []):
            url = f if str(f).startswith("http") else base + str(f)
            name = Path(str(f).split("?", 1)[0]).name
            download_file(client, url, target / name)
            print(f"downloaded {name} -> {target.relative_to(root)}")
        chal["is_downloaded"] = True
    save_config(root, cfg)
    print(f"Processed attachments for {len(cfg.get('Challenges', []))} challenges")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    root, rest = ".", []
    i = 0
    while i < len(argv):
        if argv[i] in ("-d", "--dir", "--directory") and i + 1 < len(argv):
            root = argv[i + 1]; i += 2
        else:
            rest.append(argv[i]); i += 1
    if not rest:
        print("usage: python -m ctfd [-d ROOT] {init|sync|challenges} [options]")
        return 2
    cmd, args = rest[0], rest[1:]
    if cmd == "init":
        cmd_init(root, args)
    elif cmd == "sync":
        cmd_sync(root, args)
    elif cmd == "challenges":
        cmd_challenges(root, args)
    else:
        print(f"unknown command: {cmd}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
