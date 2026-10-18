"""Unit tests for the bundled ctfd client. No network: sessions are faked."""
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import ctfd
from ctfd import CtfdClient, category, slug, load_config, save_config, download_file

CRED_KEYS = ("CTFD_TOKEN", "CTF_TOKEN", "CTFD_USERNAME", "CTF_USERNAME",
             "CTFD_PASSWORD", "CTF_PASSWORD", "CTFD_USER", "CTF_USER",
             "CTFD_PASS", "CTF_PASS")


class FakeResponse:
    def __init__(self, status=200, data=None, content_type="application/json",
                 text="", chunks=(b"hello ", b"world")):
        self.status_code = status
        self._data = data if data is not None else {}
        self.headers = {"content-type": content_type}
        self.text = text
        self._chunks = chunks

    def json(self):
        return self._data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise ctfd.requests.HTTPError(str(self.status_code))

    def iter_content(self, size):
        yield from self._chunks


class FakeSession:
    """Routes /api/v1/users/me by token header; everything else is canned."""

    def __init__(self, token_me=None, session_me=None, login_ok=True):
        self.headers = {}
        self.token_me = token_me or FakeResponse(302, content_type="text/html")
        self.session_me = session_me or FakeResponse(200, {"data": {"name": "sess-user"}})
        self.login_ok = login_ok
        self.calls = []

    def get(self, url, **kw):
        self.calls.append((url, kw))
        auth = (kw.get("headers") or {}).get("Authorization", "")
        if url.endswith("/api/v1/users/me"):
            return self.token_me if auth.startswith("Token ") else self.session_me
        if url.endswith("/login"):
            return FakeResponse(text='<input name="nonce" type="hidden" value="abc">',
                                content_type="text/html")
        return FakeResponse(content_type="application/octet-stream")

    def post(self, url, **kw):
        self.calls.append((url, kw))
        return FakeResponse(status=200 if self.login_ok else 403, text="ok",
                            content_type="text/html")


class PureHelpers(unittest.TestCase):
    def test_slug(self):
        self.assertEqual(slug("Hello World!"), "hello-world")
        self.assertEqual(slug("***"), "challenge")

    def test_category(self):
        self.assertEqual(category("Binary Exploitation"), "pwn")
        self.assertEqual(category("Web Exploitation"), "web")
        self.assertEqual(category("Cryptography"), "crypto")

    def test_config_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            save_config(d, {"CTFD": {"URL": "https://x"}, "Challenges": [{"id": 1}]})
            self.assertEqual(load_config(d)["CTFD"]["URL"], "https://x")


class Auth(unittest.TestCase):
    def setUp(self):
        patcher = mock.patch.dict(os.environ, {}, clear=False)
        patcher.start()
        self.addCleanup(patcher.stop)
        for k in CRED_KEYS:
            os.environ.pop(k, None)

    def client(self, token=None, **kw):
        c = CtfdClient("https://example.test", token)
        c.s = FakeSession(**kw)
        return c

    def test_token_success(self):
        c = self.client("T", token_me=FakeResponse(200, {"data": {"name": "tok"}}))
        self.assertEqual(c.authenticate(), ("token", "tok"))
        self.assertTrue(c.token_auth)

    def test_session_fallback_after_bad_token(self):
        os.environ.update(CTFD_USERNAME="u", CTFD_PASSWORD="p")
        c = self.client("bad")
        self.assertEqual(c.authenticate(), ("session", "sess-user"))
        self.assertTrue(c.session_auth)

    def test_bad_token_no_creds_exits(self):
        with self.assertRaises(SystemExit):
            self.client("bad").authenticate()

    def test_no_credentials_exits(self):
        with self.assertRaises(SystemExit):
            self.client().authenticate()

    def test_login_failure_exits(self):
        os.environ.update(CTFD_USERNAME="u", CTFD_PASSWORD="p")
        c = self.client(login_ok=False, session_me=FakeResponse(302, content_type="text/html"))
        with self.assertRaises(SystemExit):
            c.authenticate()
        self.assertFalse(c.session_auth)


class Downloads(unittest.TestCase):
    def stub(self):
        c = CtfdClient("https://example.test", None)
        c.s = FakeSession()
        return c

    def test_download_file_is_atomic(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "a.bin"
            download_file(self.stub(), "https://example.test/files/a.bin", dest)
            self.assertEqual(dest.read_bytes(), b"hello world")
            self.assertFalse(dest.with_name("a.bin.part").exists())

    def test_cmd_challenges_skips_existing_file(self):
        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "web" / "a" / "f.txt"
            dest.parent.mkdir(parents=True)
            dest.write_bytes(b"old")
            save_config(d, {
                "CTFD": {"URL": "https://example.test", "TOKEN": "T"},
                "Challenges": [{"id": 1, "name": "A", "category": "Web",
                                "file_urls": ["https://example.test/files/f.txt"]}],
            })
            fake = mock.Mock()
            fake.authenticate.return_value = ("token", "x")
            fake.s = FakeSession()
            with mock.patch.object(ctfd, "CtfdClient", return_value=fake):
                ctfd.cmd_challenges(d, [])
            self.assertEqual(dest.read_bytes(), b"old")
            self.assertFalse(any("f.txt" in u for u, _ in fake.s.calls))

    def test_cmd_challenges_downloads_missing_file(self):
        with tempfile.TemporaryDirectory() as d:
            save_config(d, {
                "CTFD": {"URL": "https://example.test", "TOKEN": "T"},
                "Challenges": [{"id": 1, "name": "A", "category": "Web",
                                "file_urls": ["https://example.test/files/f.txt"]}],
            })
            fake = mock.Mock()
            fake.authenticate.return_value = ("token", "x")
            fake.s = FakeSession()
            with mock.patch.object(ctfd, "CtfdClient", return_value=fake):
                ctfd.cmd_challenges(d, [])
            dest = Path(d) / "web" / "a" / "f.txt"
            self.assertEqual(dest.read_bytes(), b"hello world")

    def test_main_usage_returns_2(self):
        with mock.patch("sys.stdout"):
            self.assertEqual(ctfd.main([]), 2)


if __name__ == "__main__":
    unittest.main()
