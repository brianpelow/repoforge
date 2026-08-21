"""Tests for RepoGenerator license output."""

import hashlib

from repoforge.core.config import ScaffoldConfig
from repoforge.core.generator import RepoGenerator

CANONICAL_APACHE_BLOB = "d645695673349e3947e8e5ae42332d0ac3164cd7"
STUB = "Apache License\nVersion 2.0, January 2004\nhttp://www.apache.org/licenses/\n"


def blob_sha(data: bytes) -> str:
    """Compute a git blob SHA exactly as git does."""
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def _scaffold(tmp_path):
    config = ScaffoldConfig(name="demo-repo", output_dir=tmp_path)
    generator = RepoGenerator(config)
    generator.create_structure()
    generator.write_configs()
    return config.repo_path


def test_scaffolded_license_is_canonical_apache(tmp_path):
    """The generated LICENSE must be byte-identical to upstream Apache-2.0.

    Asserting the blob SHA rather than a marker phrase is deliberate: a CRLF
    translation on write yields a file that still reads as a license but
    hashes differently, and no detector would match it.
    """
    data = (_scaffold(tmp_path) / "LICENSE").read_bytes()
    assert blob_sha(data) == CANONICAL_APACHE_BLOB


def test_scaffolded_license_is_not_the_old_stub(tmp_path):
    """Reconstructs the stub this replaced, so the regression is proven to fail."""
    data = (_scaffold(tmp_path) / "LICENSE").read_bytes()
    assert data.decode("utf-8") != STUB
    assert blob_sha(STUB.encode()) != CANONICAL_APACHE_BLOB


def test_notice_names_the_repo(tmp_path):
    """Copyright lives in NOTICE so LICENSE stays byte-identical across repos."""
    notice = (_scaffold(tmp_path) / "NOTICE").read_text(encoding="utf-8")
    assert notice.startswith("demo-repo\n")
    assert "Apache License" in notice
