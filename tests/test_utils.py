"""Unit tests for utility functions."""

from app.utils import ensure_directory, file_exists, get_system_metadata


def test_ensure_directory(tmp_path):
    target_dir = tmp_path / "nested" / "dir"
    result = ensure_directory(target_dir)
    assert result.is_dir()
    assert target_dir.exists()


def test_file_exists(tmp_path):
    test_file = tmp_path / "test.txt"
    assert not file_exists(test_file)
    test_file.write_text("devops")
    assert file_exists(test_file)


def test_get_system_metadata():
    metadata = get_system_metadata()
    assert "hostname" in metadata
    assert "platform" in metadata
    assert "python_version" in metadata
    assert "system_time" in metadata
