"""Algorithm for grouping images by date granularity."""
import os
import datetime

class DateGroupingAlgo:
    """Handles the extraction and formatting of dates from file metadata."""

    def run(self, image_path: str, granularity: str = "month") -> dict:
        """Extracts the modification date and formats it based on granularity.

        Args:
            image_path: Path to the image file.
            granularity: Date detail level ('year', 'month', or 'day').

        Returns:
            A dictionary containing the formatted date string or an error.
        """
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
