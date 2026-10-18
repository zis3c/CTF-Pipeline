"""Unit tests for scripts/ctf-pipeline.py helpers. Temp dirs only, no network."""
import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.argv = ["ctf-pipeline.py"]  # keep import from reading a caller's argv
_spec = importlib.util.spec_from_file_location("ctf_pipeline", REPO / "scripts" / "ctf-pipeline.py")
mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mod)


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self._orig = (mod.ROOT, mod.STATE, mod.EVENT)
        mod.ROOT = self.tmp
        mod.STATE = self.tmp / ".pipeline"
        mod.EVENT = self.tmp.name

    def tearDown(self):
        mod.ROOT, mod.STATE, mod.EVENT = self._orig
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rel, data):
        p = self.tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(data if isinstance(data, str) else json.dumps(data), encoding="utf-8")
        return p


class Helpers(Base):
    def test_slug(self):
        self.assertEqual(mod.slug("Hello World"), "hello-world")
        self.assertEqual(mod.slug("@@@"), "challenge")

    def test_challenge_key(self):
        self.assertEqual(mod.challenge_key({"id": 1, "name": "A"}), ("1", "A"))

    def test_attachment_names_strips_query(self):
        item = {"files": ["/f/a.txt?sig=1", "/f/b.bin"]}
        self.assertEqual(mod.attachment_names(item), {"a.txt", "b.bin"})

    def test_diff_counts_new_removed_modified(self):
        old = [{"id": 1, "name": "A", "value": 100}, {"id": 2, "name": "B", "value": 50}]
        new = [{"id": 1, "name": "A", "value": 200}, {"id": 3, "name": "C", "value": 10}]
        self.assertEqual(mod.diff(old, new), 3)


class Archive(Base):
    def test_history_pruned_to_keep(self):
        self.write("challenges-detailed.json", [])
        for i in range(12):
            (self.tmp / ".history" / f"2020-01-{i:02d}T000000Z").mkdir(parents=True)
        mod.archive()
        kept = [p for p in (self.tmp / ".history").iterdir() if p.is_dir()]
        self.assertEqual(len(kept), mod.HISTORY_KEEP)


class Metadata(Base):
    def test_profile_reports_token_configured(self):
        self.write("challenges-detailed.json", [])
        self.write(".ctfd/config.json", {"CTFD": {"URL": "https://x", "TOKEN": "T"}})
        mod.metadata()
        profile = json.loads((self.tmp / ".ctf-profile.json").read_text(encoding="utf-8"))
        self.assertEqual(profile["token_status"], "configured")
        self.assertEqual(profile["challenge_count"], 0)


class Status(Base):
    def test_invalid_status_raises(self):
        with self.assertRaises(SystemExit):
            mod.set_status("A", "nope")

    def test_set_status_writes_marker(self):
        self.write("challenges-detailed.json", [{"id": 1, "name": "A", "category": "Web"}])
        mod.set_status("A", "solved")
        marker = self.tmp / "web" / "a" / ".solver-status"
        self.assertEqual(marker.read_text(encoding="utf-8").strip(), "solved")


class GitInit(Base):
    def test_gitignore_created_with_lock(self):
        if shutil.which("git") is None:
            self.skipTest("git not available")
        mod.init_git()
        text = (self.tmp / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".pipeline.lock", text)


if __name__ == "__main__":
    unittest.main()
