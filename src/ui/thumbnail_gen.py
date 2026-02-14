from PIL import Image
import io

class ThumbnailGenerator:
    """Utility class to generate thumbnails from image files."""
    
    @staticmethod
    def generate(image_path, size=(150, 150)):
        """
        Generates a thumbnail for the given image and returns it as bytes.
        """
        try:
            with Image.open(image_path) as img:
                # Use thumbnail() which maintains aspect ratio
                img.thumbnail(size)
                
                # Save to buffer
                buffer = io.BytesIO()
                # Use JPEG for thumbnails to save space, or keep original format?
                # JPEG is generally smaller.
                img.save(buffer, format="JPEG", quality=85)
                return buffer.getvalue()
        except Exception as e:
            print(f"Error generating thumbnail for {image_path}: {e}")
            return None
