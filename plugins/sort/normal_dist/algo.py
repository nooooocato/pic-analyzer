import numpy as np
from typing import List, Dict, Any
from src.plugin.base import SortPlugin

class NormalDistributionPlugin(SortPlugin):
    """Refactored Normal Distribution Sort Plugin using the new logic-only interface."""

    @property
    def name(self) -> str:
        return "Normal Distribution"

    @property
    def description(self) -> str:
        return "Show items closest to the mean value first."

    def sort(self, items: List[Dict[str, Any]], metric_key: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sorts items by their absolute distance from the mean of the metric."""
        if not items:
            return []
        values = [float(item.get(metric_key, 0)) for item in items]
        mean = np.mean(values)
        return sorted(items, key=lambda x: abs(float(x.get(metric_key, 0)) - mean))

    def run(self, image_path: str) -> dict:
        return {}
