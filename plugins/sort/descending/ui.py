from base import BasePlugin
from sort.base import BaseSortPlugin
from sort.descending.algo import DescendingSort

class DescendingPlugin(BasePlugin, BaseSortPlugin):
    @property
    def name(self) -> str:
        return "Descending (Ext)"

    @property
    def description(self) -> str:
        return "Sort items from highest to lowest value (Externalized)."

    def sort(self, items, metric_key):
        return DescendingSort().sort(items, metric_key)

    def run(self, image_path: str) -> dict:
        return {}

    def initialize_ui(self, main_window) -> None:
        main_window.register_sort_plugin(self)
