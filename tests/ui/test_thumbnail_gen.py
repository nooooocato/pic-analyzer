import pytest
from PIL import Image
import io
import os
from src.ui.thumbnail_gen import ThumbnailGenerator

@pytest.fixture
def test_image(tmp_path):
    img_path = tmp_path / "test.jpg"
    img = Image.new('RGB', (1000, 1000), color='red')
    img.save(img_path)
    return str(img_path)

def test_generate_thumbnail(test_image):
    gen = ThumbnailGenerator()
    thumb_bytes = gen.generate(test_image, size=(150, 150))
    
    assert isinstance(thumb_bytes, bytes)
    assert len(thumb_bytes) > 0
    
    # Verify it's a valid image
    thumb_img = Image.open(io.BytesIO(thumb_bytes))
    assert thumb_img.size[0] <= 150
    assert thumb_img.size[1] <= 150

def test_generate_thumbnail_invalid_path():
    gen = ThumbnailGenerator()
    thumb_bytes = gen.generate("invalid_path.jpg")
    assert thumb_bytes is None
