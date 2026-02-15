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

    def run(self, image_path: str, granularity: str = "month") -> dict:
        if not os.path.exists(image_path):
            return {"error": "File not found"}
        
        mtime = os.path.getmtime(image_path)
        dt = datetime.datetime.fromtimestamp(mtime)
        
        if granularity == "year":
            date_str = dt.strftime('%Y')
        elif granularity == "day":
            date_str = dt.strftime('%Y-%m-%d')
        else: # month
            date_str = dt.strftime('%Y-%m')
        
        return {"date": date_str}
