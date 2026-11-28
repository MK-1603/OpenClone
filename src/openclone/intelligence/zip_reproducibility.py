"""OpenClone Deterministic ZIP Packaging Engine.

Provides byte-level reproducible archive generation across operating systems
and Python runtimes by normalizing:
1. Path separators to POSIX '/'
2. Lexicographical file ordering
3. Fixed timestamps (1980-01-01 00:00:00 UTC or SOURCE_DATE_EPOCH)
4. UNIX host system attributes (create_system = 3)
5. Normalized file modes (0o644 for files, 0o755 for directories/executables)
6. Dual verification: archive SHA-256 and invariant content manifest SHA-256.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import time
import zipfile
from typing import Dict, List, Optional, Tuple, Union


DEFAULT_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


def get_normalized_timestamp() -> Tuple[int, int, int, int, int, int]:
    """Retrieve normalized timestamp tuple from SOURCE_DATE_EPOCH or default."""
    source_epoch = os.environ.get("SOURCE_DATE_EPOCH")
    if source_epoch:
        try:
            utc_time = time.gmtime(int(source_epoch))
            return (
                utc_time.tm_year,
                utc_time.tm_mon,
                utc_time.tm_mday,
                utc_time.tm_hour,
                utc_time.tm_min,
                utc_time.tm_sec,
            )
        except (ValueError, OverflowError):
            pass
    return DEFAULT_TIMESTAMP


def compute_content_manifest(source_dir: Union[str, Path]) -> Dict[str, str]:
    """Compute sha256 for all files in directory, keyed by posix relative path."""
    source = Path(source_dir).resolve()
    manifest: Dict[str, str] = {}
    for path in sorted(source.rglob("*")):
        if path.is_file():
            rel_posix = path.relative_to(source).as_posix()
            h = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(65536), b""):
                    h.update(chunk)
            manifest[rel_posix] = h.hexdigest()
    return manifest


def compute_manifest_digest(manifest: Dict[str, str]) -> str:
    """Compute overall sha256 digest of sorted file content manifest."""
    h = hashlib.sha256()
    for rel_path in sorted(manifest.keys()):
        line = f"{manifest[rel_path]}  {rel_path}\n"
        h.update(line.encode("utf-8"))
    return h.hexdigest()


def create_deterministic_zip(
    source_dir: Union[str, Path],
    output_zip: Union[str, Path],
    compression: int = zipfile.ZIP_DEFLATED,
    compresslevel: int = 9,
) -> Dict[str, Union[str, int]]:
    """Build a byte-for-byte deterministic ZIP archive from source_dir.

    Args:
        source_dir: Root directory to package.
        output_zip: Destination ZIP file path.
        compression: zipfile.ZIP_DEFLATED or zipfile.ZIP_STORED.
        compresslevel: Compression level (default 9 for max deterministic compression).

    Returns:
        Dict containing:
            - zip_path: Path to generated ZIP
            - zip_sha256: SHA-256 of the generated ZIP file
            - manifest_sha256: Invariant SHA-256 of content manifest
            - file_count: Number of files archived
    """
    source = Path(source_dir).resolve()
    dest = Path(output_zip).resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)

    timestamp = get_normalized_timestamp()
    all_entries: List[Path] = sorted(source.rglob("*"), key=lambda p: p.relative_to(source).as_posix())

    with zipfile.ZipFile(dest, "w", compression=compression, compresslevel=compresslevel) as zf:
        for path in all_entries:
            rel_posix = path.relative_to(source).as_posix()
            if path.is_dir():
                zip_path = rel_posix + "/"
                zinfo = zipfile.ZipInfo(filename=zip_path, date_time=timestamp)
                zinfo.create_system = 3  # UNIX
                # Directory mode 0o755 + directory bit (0o040000)
                zinfo.external_attr = (0o755 << 16) | stat.S_IFDIR
                zf.writestr(zinfo, b"")
            elif path.is_file():
                zinfo = zipfile.ZipInfo(filename=rel_posix, date_time=timestamp)
                zinfo.create_system = 3  # UNIX
                # Determine executable status
                is_executable = bool(path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
                mode = 0o755 if is_executable else 0o644
                zinfo.external_attr = (mode << 16) | stat.S_IFREG
                zinfo.compress_type = compression

                with open(path, "rb") as f:
                    content = f.read()
                zf.writestr(zinfo, content, compress_type=compression)

    # Compute ZIP file hash
    h_zip = hashlib.sha256()
    with open(dest, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h_zip.update(chunk)
    zip_sha256 = h_zip.hexdigest()

    manifest = compute_content_manifest(source)
    manifest_sha256 = compute_manifest_digest(manifest)

    # Write sidecar hashes
    dest.with_suffix(".zip.sha256").write_text(f"{zip_sha256}  {dest.name}\n", encoding="utf-8")
    dest.with_suffix(".manifest.sha256").write_text(f"{manifest_sha256}  manifest\n", encoding="utf-8")

    return {
        "zip_path": str(dest),
        "zip_sha256": zip_sha256,
        "manifest_sha256": manifest_sha256,
        "file_count": len(manifest),
    }
