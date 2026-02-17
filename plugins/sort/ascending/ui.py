from plugins.base import BasePlugin
from plugins.sort.base import BaseSortPlugin
from plugins.sort.ascending.algo import AscendingSort

class AscendingPlugin(BasePlugin, BaseSortPlugin):
    """Plugin for sorting items in ascending order based on a metric.

    This plugin implements both the general BasePlugin interface for discovery
    and the BaseSortPlugin interface for integration into the sorting system.
    """

    @property
    def name(self) -> str:
        """Returns the display name of the plugin."""
        return "Ascending (Ext)"

    @property
    def description(self) -> str:
        """Returns the description of the sorting algorithm."""
        return "Sort items from lowest to highest value (Externalized)."

    def sort(self, items, metric_key):
        """Performs the sorting operation.

        Args:
            items (list): List of dictionaries containing image metadata.
            metric_key (str): The key to sort by.

        Returns:
            list: The sorted list of items.
        """
        return AscendingSort().sort(items, metric_key)

    def run(self, image_path: str) -> dict:
        """Empty implementation of analysis for sorting-only plugin."""
        return {}

    def initialize_ui(self, main_window) -> None:
        """Registers the sorting algorithm with the MainWindow."""
        main_window.register_sort_plugin(self)
