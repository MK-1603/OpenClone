import tempfile
import unittest
import zipfile
from pathlib import Path
from src.openclone.intelligence.zip_reproducibility import (
    create_deterministic_zip,
    compute_content_manifest,
    compute_manifest_digest,
    DEFAULT_TIMESTAMP,
)


class TestZipReproducibility(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)
        self.src = self.base / "src"
        self.src.mkdir(parents=True)
        # Create sample nested structure
        (self.src / "b_dir").mkdir()
        (self.src / "a_dir").mkdir()
        (self.src / "b_dir" / "file2.txt").write_text("Hello World B", encoding="utf-8")
        (self.src / "a_dir" / "file1.txt").write_text("Hello World A", encoding="utf-8")
        (self.src / "root.md").write_text("# Root Project", encoding="utf-8")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_reproducible_sha256_across_runs(self):
        out1 = self.base / "archive1.zip"
        out2 = self.base / "archive2.zip"

        res1 = create_deterministic_zip(self.src, out1)
        res2 = create_deterministic_zip(self.src, out2)

        self.assertEqual(res1["zip_sha256"], res2["zip_sha256"])
        self.assertEqual(res1["manifest_sha256"], res2["manifest_sha256"])
        self.assertEqual(res1["file_count"], 3)
        self.assertTrue(out1.with_suffix(".zip.sha256").exists())
        self.assertTrue(out1.with_suffix(".manifest.sha256").exists())

    def test_zip_stored_reproducibility(self):
        out1 = self.base / "stored1.zip"
        out2 = self.base / "stored2.zip"

        res1 = create_deterministic_zip(self.src, out1, compression=zipfile.ZIP_STORED)
        res2 = create_deterministic_zip(self.src, out2, compression=zipfile.ZIP_STORED)

        self.assertEqual(res1["zip_sha256"], res2["zip_sha256"])
        self.assertEqual(res1["manifest_sha256"], res2["manifest_sha256"])

    def test_zip_header_normalization(self):
        out = self.base / "normalized.zip"
        create_deterministic_zip(self.src, out)

        with zipfile.ZipFile(out, "r") as zf:
            for info in zf.infolist():
                # Verify UNIX host attribute
                self.assertEqual(info.create_system, 3)
                # Verify fixed date_time
                self.assertEqual(info.date_time, DEFAULT_TIMESTAMP)
                # Verify POSIX separator
                self.assertNotIn("\\", info.filename)

    def test_manifest_computation(self):
        manifest = compute_content_manifest(self.src)
        self.assertIn("a_dir/file1.txt", manifest)
        self.assertIn("b_dir/file2.txt", manifest)
        self.assertIn("root.md", manifest)

        digest1 = compute_manifest_digest(manifest)
        digest2 = compute_manifest_digest(manifest)
        self.assertEqual(digest1, digest2)


if __name__ == "__main__":
    unittest.main()
