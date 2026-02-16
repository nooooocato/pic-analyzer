from base import BasePlugin
from sort.base import BaseSortPlugin
from sort.ascending.algo import AscendingSort

class AscendingPlugin(BasePlugin, BaseSortPlugin):
    @property
    def name(self) -> str:
        return "Ascending (Ext)"

    @property
    def description(self) -> str:
        return "Sort items from lowest to highest value (Externalized)."

    def sort(self, items, metric_key):
        return AscendingSort().sort(items, metric_key)

    def run(self, image_path: str) -> dict:
        return {}

    def initialize_ui(self, main_window) -> None:
        main_window.register_sort_plugin(self)
