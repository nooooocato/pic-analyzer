from src.plugin.base import BasePlugin
from plugins.group.date_grouping.algo import DateGroupingAlgo

class DateGroupingPlugin(BasePlugin):
    """Plugin for grouping items by their file modification date.

    Injects menu items into the 'View/Group By' menu to allow users to group
    images by Year, Month, or Day.
    """

    @property
    def name(self) -> str:
        """Returns the display name of the plugin."""
        return "Date Grouping (Ext)"

    @property
    def description(self) -> str:
        """Returns a brief description of the grouping functionality."""
        return "Groups images by their modification date (Externalized)."

    def run(self, image_path: str, granularity: str = "month") -> dict:
        """Extracts the date from the image file.

        Args:
            image_path (str): Path to the image file.
            granularity (str): The level of date detail (year, month, day).

        Returns:
            dict: Results containing the formatted date string.
        """
        return DateGroupingAlgo().run(image_path, granularity)

    def initialize_ui(self, main_window) -> None:
        """Injects date grouping actions into the main menu."""
        group_menu = main_window.get_menu("View/Group By")
        date_menu = group_menu.addMenu("Date")
        
        # We need to reach the gallery to set grouping
        # This is a bit of a leap, but main_window.layout_engine.gallery is available    
        gallery = main_window.layout_engine.gallery
        
        date_menu.addAction("Year").triggered.connect(lambda: gallery.set_grouping(self, "year"))
        date_menu.addAction("Month").triggered.connect(lambda: gallery.set_grouping(self, "month"))
        date_menu.addAction("Day").triggered.connect(lambda: gallery.set_grouping(self, "day"))
