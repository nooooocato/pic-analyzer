import os
import datetime
from .base import BasePlugin

class DateGroupingPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Date Grouping"

    @property
    def description(self) -> str:
        return "Groups images by their modification date (YYYY-MM-DD)."

    def run(self, image_path: str) -> dict:
        if not os.path.exists(image_path):
            return {"error": "File not found"}
        
        mtime = os.path.getmtime(image_path)
        date_str = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        
        return {"date": date_str}
