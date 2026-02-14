from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class ThumbnailGenerator:
    """Utility class to generate thumbnails from image files."""
    
    @staticmethod
    def generate(image_path, size=(150, 150)):
        """
        Generates a thumbnail for the given image and returns it as bytes.
        """
        try:
            logger.debug(f"Opening image for thumbnail: {image_path}")
            with Image.open(image_path) as img:
                # Convert to RGB if necessary (e.g., for GIFs/P-mode images)
                if img.mode in ("P", "RGBA"):
                    img = img.convert("RGB")
                    
                # Use thumbnail() which maintains aspect ratio
                img.thumbnail(size)
                
                # Save to buffer
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG", quality=85)
                return buffer.getvalue()
        except Exception as e:
            logger.error(f"Error generating thumbnail for {image_path}: {e}")
            return None
