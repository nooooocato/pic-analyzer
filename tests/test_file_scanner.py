import pytest
import os
import shutil
from PySide6.QtCore import QCoreApplication
from src.file_scanner import FolderScanner

@pytest.fixture
def temp_image_dir(tmp_path):
    # Create a nested directory structure with some "images"
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    (img_dir / "test1.jpg").write_text("fake data")
    (img_dir / "test2.png").write_text("fake data")
    (img_dir / "not_an_image.txt").write_text("fake data")
    
    sub_dir = img_dir / "sub"
    sub_dir.mkdir()
    # Need real image data for Pillow to work
    from PIL import Image
    import io
    def save_img(path):
        img = Image.new('RGB', (10, 10), color='red')
        img.save(path)
    
    save_img(img_dir / "test1.jpg")
    save_img(img_dir / "test2.png")
    save_img(sub_dir / "test3.webp")
    save_img(sub_dir / "test4.BMP")
    (img_dir / "not_an_image.txt").write_text("fake data")
    
    return str(img_dir)

def test_folder_scanner_finds_images(temp_image_dir, qtbot):
    found_files = []
    
    scanner = FolderScanner(temp_image_dir)
    
    # Connect signal to collect found files and thumbnails
    scanner.signals.file_found.connect(lambda p, t: found_files.append((p, t)))
    
    # Run the scanner logic directly
    scanner.run()
    
    assert len(found_files) == 4
    for path, thumb in found_files:
        assert isinstance(path, str)
        assert isinstance(thumb, bytes)
        assert len(thumb) > 0

def test_folder_scanner_finished_signal(temp_image_dir, qtbot):
    scanner = FolderScanner(temp_image_dir)
    
    with qtbot.waitSignal(scanner.signals.finished, timeout=1000):
        scanner.run()

def test_folder_scanner_error(qtbot, monkeypatch):
    scanner = FolderScanner("/invalid/path")
    
    def mock_walk(path):
        raise OSError("Permission denied")
    
    import os
    monkeypatch.setattr(os, "walk", mock_walk)
    
    with qtbot.waitSignal(scanner.signals.error, timeout=1000) as blocker:
        scanner.run()
    
    assert "Permission denied" in blocker.args[0]
