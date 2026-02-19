import json
from peewee import SqliteDatabase
from .models import db_proxy, Workspace, Image, AnalysisResult
import os

class DBManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.db = None
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database connection and creates tables if they don't exist."""
        self.db = SqliteDatabase(self.db_path)
        db_proxy.initialize(self.db)
        
        # Ensure tables exist
        self.db.create_tables([Workspace, Image, AnalysisResult])

    def switch_database(self, new_db_path: str):
        """Closes the current connection and opens a new one."""
        if self.db:
            self.db.close()
        
        self.db_path = new_db_path
        self._initialize_db()

    def get_db(self):
        return self.db

    def manage_workspace(self, action: str, data: dict):
        """Manage Workspace records: create, load, delete."""
        if action == "create":
            ws, created = Workspace.get_or_create(
                name=data["name"], 
                defaults={"path": data["path"]}
            )
            if not created and ws.path != data["path"]:
                ws.path = data["path"]
                ws.save()
            return ws
        elif action == "load":
            return Workspace.get(Workspace.name == data["name"])
        elif action == "delete":
            try:
                ws = Workspace.get(Workspace.name == data["name"])
                ws.delete_instance(recursive=True)
                return True
            except Workspace.DoesNotExist:
                return False
        return None

    def upsert_image(self, metadata: dict, analysis_data: dict):
        """Insert or update an image and its analysis results."""
        with self.db.atomic():
            img, created = Image.get_or_create(
                path=metadata["path"],
                defaults={
                    "filename": metadata["filename"],
                    "file_size": metadata.get("file_size"),
                    "created_at": metadata.get("created_at"),
                    "modified_at": metadata.get("modified_at"),
                    "workspace": metadata["workspace"],
                    "thumbnail": metadata.get("thumbnail")
                }
            )
            
            if not created:
                # Update existing image record
                img.filename = metadata["filename"]
                img.file_size = metadata.get("file_size")
                if "created_at" in metadata:
                    img.created_at = metadata["created_at"]
                if "modified_at" in metadata:
                    img.modified_at = metadata["modified_at"]
                if "thumbnail" in metadata:
                    img.thumbnail = metadata["thumbnail"]
                img.save()
            
            # Upsert AnalysisResult (simplification: one AnalysisResult per image per plugin for now, 
            # or just one global one. The spec says AnalysisResult has plugin_name).
            # If analysis_data is provided, we merge it or replace it?
            # Existing code used result_key/result_value pairs.
            # New model has result_data (JSON).
            
            # For simplicity, we'll store all results under "default" plugin for now if not specified.
            plugin_name = metadata.get("plugin_name", "default")
            
            ar, ar_created = AnalysisResult.get_or_create(
                image=img,
                plugin_name=plugin_name,
                defaults={"result_data": json.dumps(analysis_data)}
            )
            
            if not ar_created and analysis_data:
                # Merge or replace? Let's merge for flexibility
                current_data = json.loads(ar.result_data)
                current_data.update(analysis_data)
                ar.result_data = json.dumps(current_data)
                ar.save()
                
            return img

    def query_images(self, filters: dict = None, group_by: str = None):
        """Query images and return a Peewee Select object."""
        query = Image.select()
        
        if filters:
            for field_name, value in filters.items():
                if hasattr(Image, field_name):
                    field = getattr(Image, field_name)
                    query = query.where(field == value)
        
        # Note: group_by implementation can be complex for plugins, 
        # but basic support here:
        if group_by and hasattr(Image, group_by):
            query = query.group_by(getattr(Image, group_by))
            
        return query

    def update_metrics(self, image_id: int, metrics: dict):
        """Update specific metrics for an image."""
        img = Image.get_by_id(image_id)
        # Use upsert_image logic or specialized update
        self.upsert_image({"path": img.path, "filename": img.filename, "workspace": img.workspace}, metrics)

    def get_image_metadata(self, path: str) -> dict:
        """Fetches all stored metadata and analysis results for a given image path."""
        try:
            img = Image.get(Image.path == path)
        except Image.DoesNotExist:
            return {}
            
        metadata = {
            "Filename": img.filename,
            "Size": f"{img.file_size / 1024:.2f} KB" if img.file_size else "Unknown",
            "Modified": img.modified_at
        }
        
        # Merge all analysis results
        for ar in img.analysis_results:
            try:
                data = json.loads(ar.result_data)
                for key, val in data.items():
                    # Try to format numeric values for display
                    if isinstance(val, (int, float)):
                        metadata[key] = f"{val:.4f}" if isinstance(val, float) else str(val)
                    else:
                        metadata[key] = str(val)
            except (ValueError, TypeError, json.JSONDecodeError):
                continue
                
        return metadata

    def get_numeric_metrics(self) -> list[str]:
        """Returns a list of keys that contain numeric values across all images."""
        numeric_keys = {"file_size", "modified_at"}
        
        # Scan AnalysisResults to find other numeric keys
        for ar in AnalysisResult.select(AnalysisResult.result_data):
            try:
                data = json.loads(ar.result_data)
                for key, val in data.items():
                    try:
                        float(val)
                        numeric_keys.add(key)
                    except (ValueError, TypeError):
                        pass
            except (json.JSONDecodeError, TypeError):
                continue
                
        return sorted(list(numeric_keys))

    def get_metric_values(self, metric_key: str) -> dict[str, float]:
        """Returns a mapping of image path to its numeric value for the given metric."""
        results = {}
        
        if metric_key in ["file_size", "modified_at"]:
            for img in Image.select(Image.path, getattr(Image, metric_key)):
                val = getattr(img, metric_key)
                results[img.path] = float(val) if val is not None else 0.0
        else:
            # Join Image and AnalysisResult to get path and result_data
            query = (Image
                     .select(Image.path, AnalysisResult.result_data)
                     .join(AnalysisResult))
            
            for row in query:
                try:
                    data = json.loads(row.analysis_results[0].result_data) # This might be problematic if multiple ARs
                    if metric_key in data:
                        val = data[metric_key]
                        try:
                            results[row.path] = float(val)
                        except (ValueError, TypeError):
                            pass
                except (IndexError, json.JSONDecodeError, TypeError):
                    continue
                    
            # Actually, the above join logic is slightly flawed for multiple ARs per image.
            # Let's do it more robustly:
            results = {}
            if metric_key in ["file_size", "modified_at"]:
                for img in Image.select(Image.path, getattr(Image, metric_key)):
                    val = getattr(img, metric_key)
                    results[img.path] = float(val) if val is not None else 0.0
            else:
                for ar in AnalysisResult.select(AnalysisResult.result_data, Image.path).join(Image):
                    try:
                        data = json.loads(ar.result_data)
                        if metric_key in data:
                            val = data[metric_key]
                            try:
                                results[ar.image.path] = float(val)
                            except (ValueError, TypeError):
                                pass
                    except (json.JSONDecodeError, TypeError):
                        continue
        return results
