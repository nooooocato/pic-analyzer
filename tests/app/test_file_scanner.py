import pytest
import os
import shutil
from PySide6.QtCore import QCoreApplication
from src.app.file_scanner import FolderScanner

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

def test_folder_scanner_persistence(temp_image_dir, qtbot, tmp_path):
    db_path = str(tmp_path / "persistence.db")
    from src.db.manager import DBManager
    from src.db.models import Image
    db_manager = DBManager(db_path) # Initialize schema
    
    scanner = FolderScanner(temp_image_dir, db_path)
    scanner.run()
    
    # Verify data is in DB
    assert Image.select().count() == 4
    assert Image.select().where(Image.thumbnail.is_null(False)).count() == 4
    
    # Run again, should load from DB (we can mock thumbnail_gen to verify)
    import unittest.mock as mock
    with mock.patch('src.ui.thumbnail_gen.ThumbnailGenerator.generate') as mock_gen:
        scanner2 = FolderScanner(temp_image_dir, db_path)
        scanner2.run()
        # Should NOT call generate because it loads from DB
        assert mock_gen.call_count == 0

    # Modify a file
    img_path = os.path.join(temp_image_dir, "test1.jpg")
    # Wait a bit to ensure mtime changes if system resolution is low
    import time
    time.sleep(0.1)
    with open(img_path, "wb") as f:
        from PIL import Image
        img = Image.new('RGB', (20, 20), color='blue') # Different content
        img.save(f, format="JPEG")
    
    with mock.patch('src.ui.thumbnail_gen.ThumbnailGenerator.generate') as mock_gen:
        mock_gen.return_value = b"new_thumb"
        scanner3 = FolderScanner(temp_image_dir, db_path)
        scanner3.run()
        # Should call generate exactly once for the modified file
        assert mock_gen.call_count == 1

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

def test_folder_scanner_cancellation(temp_image_dir, qtbot):
    scanner = FolderScanner(temp_image_dir)
    found_files = []
    scanner.signals.file_found.connect(lambda p, t: found_files.append(p))
    
    # Mock walk to simulate progress then cancellation
    import os
    original_walk = os.walk
    
    def mock_walk(path):
        for root, dirs, files in original_walk(path):
            for file in files:
                # Cancel after finding first file
                scanner.cancel()
                yield root, dirs, [file]
    
    import unittest.mock as mock
    with mock.patch('os.walk', side_effect=mock_walk):
        scanner.run()
    
    # Should stop early
    assert len(found_files) <= 1
