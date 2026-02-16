import os
import datetime

class DateGroupingAlgo:
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
