import os
import shutil
import sys

def hide_file(path):
    """
    Ensures a file is hidden on Windows, Linux, Android, and macOS.
    On Unix-based systems, it relies on the '.' prefix (should be added by caller).
    On Windows, it sets the FILE_ATTRIBUTE_HIDDEN attribute.
    """
    if not os.path.exists(path):
        return
    
    if sys.platform == 'win32':
        import ctypes
        # Set file attribute to hidden (0x02)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        success = ctypes.windll.kernel32.SetFileAttributesW(path, FILE_ATTRIBUTE_HIDDEN)
        return bool(success)
    return True

class FileManager:
    """Provides utilities for safe file operations, including conflict resolution."""

    def safe_move(self, src_path: str, dst_path: str, conflict_policy: str = 'ask') -> str:
        """Moves a file from src to dst using the specified conflict policy.

        Args:
            src_path (str): The absolute path to the source file.
            dst_path (str): The absolute path to the destination file.
            conflict_policy (str): How to handle existing destination files.
                Options: 'overwrite', 'rename', 'skip', 'ask'.
                Note: 'ask' currently raises FileExistsError for UI handling.

        Returns:
            str: The final path where the file was moved, or None if skipped.

        Raises:
            FileNotFoundError: If the source file does not exist.
            FileExistsError: If the destination exists and policy is 'ask'.
        """
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source file not found: {src_path}")

        if os.path.exists(dst_path):
            if conflict_policy == 'overwrite':
                os.remove(dst_path)
            elif conflict_policy == 'rename':
                dst_path = self._generate_unique_path(dst_path)
            elif conflict_policy == 'skip':
                return None
            else:
                # 'ask' would trigger a UI dialog, for now we raise to let caller handle
                raise FileExistsError(f"Destination already exists: {dst_path}")

        shutil.move(src_path, dst_path)
        return dst_path

    def _generate_unique_path(self, path: str) -> str:
        """Generates a unique file path by appending a counter.

        Args:
            path (str): The original file path.

        Returns:
            str: A unique path that does not currently exist on disk.
        """
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path
