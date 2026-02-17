from src.plugin.base import BasePlugin
from plugins.sort.base import BaseSortPlugin
from plugins.sort.descending.algo import DescendingSort

class DescendingPlugin(BasePlugin, BaseSortPlugin):
    """Plugin for sorting items in descending order based on a metric.

    This plugin implements both the general BasePlugin interface for discovery
    and the BaseSortPlugin interface for integration into the sorting system.
    """

    @property
    def name(self) -> str:
        """Returns the display name of the plugin."""
        return "Descending (Ext)"

    @property
    def description(self) -> str:
        """Returns the description of the sorting algorithm."""
        return "Sort items from highest to lowest value (Externalized)."

    def sort(self, items, metric_key):
        """Performs the sorting operation.

        Args:
            items (list): List of dictionaries containing image metadata.
            metric_key (str): The key to sort by.

        Returns:
            list: The sorted list of items.
        """
        return DescendingSort().sort(items, metric_key)

    def run(self, image_path: str) -> dict:
        """Empty implementation of analysis for sorting-only plugin."""
        return {}

    def initialize_ui(self, main_window) -> None:
        """Registers the sorting algorithm with the MainWindow."""
        main_window.register_sort_plugin(self)
