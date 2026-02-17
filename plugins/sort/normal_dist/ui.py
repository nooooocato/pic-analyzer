from plugins.base import BasePlugin
from plugins.sort.base import BaseSortPlugin
from plugins.sort.normal_dist.algo import NormalDistributionSort

class NormalDistributionPlugin(BasePlugin, BaseSortPlugin):
    """Plugin for sorting items by their distance from the mean (Normal Distribution).

    This plugin implements both the general BasePlugin interface for discovery
    and the BaseSortPlugin interface for integration into the sorting system.
    """

    @property
    def name(self) -> str:
        """Returns the display name of the plugin."""
        return "Normal Distribution (Ext)"

    @property
    def description(self) -> str:
        """Returns the description of the sorting algorithm."""
        return "Show items closest to the mean value first (Externalized)."

    def sort(self, items, metric_key):
        """Performs the sorting operation.

        Args:
            items (list): List of dictionaries containing image metadata.
            metric_key (str): The key to sort by.

        Returns:
            list: The sorted list of items.
        """
        return NormalDistributionSort().sort(items, metric_key)

    def get_stats(self, items, metric_key):
        """Calculates statistical metadata for the sort.

        Args:
            items (list): List of dictionaries containing image metadata.
            metric_key (str): The key to calculate stats for.

        Returns:
            dict: Statistical results (e.g., mean, sigma).
        """
        return NormalDistributionSort().get_stats(items, metric_key)

    def run(self, image_path: str) -> dict:
        """Empty implementation of analysis for sorting-only plugin."""
        return {}

    def initialize_ui(self, main_window) -> None:
        """Registers the sorting algorithm with the MainWindow."""
        main_window.register_sort_plugin(self)
