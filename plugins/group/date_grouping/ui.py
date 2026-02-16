from base import BasePlugin
from group.date_grouping.algo import DateGroupingAlgo

class DateGroupingPlugin(BasePlugin):
    @property
    def name(self) -> str:
        return "Date Grouping (Ext)"

    @property
    def description(self) -> str:
        return "Groups images by their modification date (Externalized)."

    def run(self, image_path: str, granularity: str = "month") -> dict:
        return DateGroupingAlgo().run(image_path, granularity)

    def initialize_ui(self, main_window) -> None:
        group_menu = main_window.get_menu("View/Group By")
        date_menu = group_menu.addMenu("Date")
        
        # We need to reach the gallery to set grouping
        # This is a bit of a leap, but main_window.layout_engine.gallery is available
        gallery = main_window.layout_engine.gallery
        
        date_menu.addAction("Year").triggered.connect(lambda: gallery.set_grouping(self, "year"))
        date_menu.addAction("Month").triggered.connect(lambda: gallery.set_grouping(self, "month"))
        date_menu.addAction("Day").triggered.connect(lambda: gallery.set_grouping(self, "day"))
