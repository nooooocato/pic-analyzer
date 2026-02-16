from base import BasePlugin
from sort.base import BaseSortPlugin
from sort.normal_dist.algo import NormalDistributionSort

class NormalDistributionPlugin(BasePlugin, BaseSortPlugin):
    @property
    def name(self) -> str:
        return "Normal Distribution (Ext)"

    @property
    def description(self) -> str:
        return "Show items closest to the mean value first (Externalized)."

    def sort(self, items, metric_key):
        return NormalDistributionSort().sort(items, metric_key)

    def get_stats(self, items, metric_key):
        return NormalDistributionSort().get_stats(items, metric_key)

    def run(self, image_path: str) -> dict:
        return {}

    def initialize_ui(self, main_window) -> None:
        main_window.register_sort_plugin(self)
