import pytest
import os
import shutil
from src.app.file_ops import FileManager

def test_safe_move_basic(tmp_path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()
    
    test_file = src_dir / "test.txt"
    test_file.write_text("hello")
    
    fm = FileManager()
    # Mocking the conflict resolution to always return 'overwrite' for basic test
    fm.safe_move(str(test_file), str(dst_dir / "test.txt"), conflict_policy='overwrite')
    
    assert not test_file.exists()
    assert (dst_dir / "test.txt").exists()
    assert (dst_dir / "test.txt").read_text() == "hello"

def test_safe_move_conflict_rename(tmp_path):
    src_dir = tmp_path / "src"
    dst_dir = tmp_path / "dst"
    src_dir.mkdir()
    dst_dir.mkdir()
    
    src_file = src_dir / "test.txt"
    src_file.write_text("new content")
    
    dst_file = dst_dir / "test.txt"
    dst_file.write_text("old content")
    
    fm = FileManager()
    # Policy 'rename' should produce test_1.txt
    fm.safe_move(str(src_file), str(dst_file), conflict_policy='rename')
    
    assert (dst_dir / "test.txt").read_text() == "old content"
    assert (dst_dir / "test_1.txt").exists()
    assert (dst_dir / "test_1.txt").read_text() == "new content"

def test_safe_move_conflict_skip(tmp_path):
    src_file = tmp_path / "src.txt"
    src_file.write_text("new")
    dst_file = tmp_path / "dst.txt"
    dst_file.write_text("old")
    
    fm = FileManager()
    result = fm.safe_move(str(src_file), str(dst_file), conflict_policy='skip')
    
    assert result is None
    assert src_file.exists()
    assert dst_file.read_text() == "old"

def test_safe_move_conflict_ask_raises(tmp_path):
    src_file = tmp_path / "src.txt"
    src_file.write_text("new")
    dst_file = tmp_path / "dst.txt"
    dst_file.write_text("old")
    
    fm = FileManager()
    with pytest.raises(FileExistsError):
        fm.safe_move(str(src_file), str(dst_file), conflict_policy='ask')

def test_safe_move_src_not_found():
    fm = FileManager()
    with pytest.raises(FileNotFoundError):
        fm.safe_move("non_existent.txt", "dst.txt")
