import os
import shutil

class FileManager:
    def safe_move(self, src_path, dst_path, conflict_policy='ask'):
        """
        Moves a file from src to dst. 
        conflict_policy: 'overwrite', 'rename', 'skip', 'ask'
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
                # 'ask' would trigger a UI dialog, for now we raise or default
                # In actual implementation, this might callback to a UI handler
                raise FileExistsError(f"Destination already exists: {dst_path}")

        shutil.move(src_path, dst_path)
        return dst_path

    def _generate_unique_path(self, path):
        base, ext = os.path.splitext(path)
        counter = 1
        new_path = f"{base}_{counter}{ext}"
        while os.path.exists(new_path):
            counter += 1
            new_path = f"{base}_{counter}{ext}"
        return new_path
