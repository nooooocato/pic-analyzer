"""Algorithm for sorting items based on proximity to the mean (Normal Distribution)."""
import numpy as np
from typing import List, Dict, Any

class NormalDistributionSort:
    """Implementation of a sort algorithm centered around the distribution mean."""

    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        """Sorts items by their absolute distance from the mean of the metric.

        Args:
            items: List of dictionaries to sort.
            metric_key: The metric key used for mean calculation and sorting.

        Returns:
            A list of items sorted by proximity to the mean.
        """
        if not items:
            return []
        values = [float(item.get(metric_key, 0)) for item in items]
        mean = np.mean(values)
        return sorted(items, key=lambda x: abs(float(x.get(metric_key, 0)) - mean))

    def get_stats(self, items: List[Dict[str, Any]], metric_key: str) -> Dict[str, Any]:
        """Calculates statistical metrics for the given items.

        Args:
            items: List of dictionaries containing metadata.
            metric_key: The metric key to analyze.

        Returns:
            A dictionary containing the mean and standard deviation (sigma).
        """
        if not items:
            return {"mean": 0, "sigma": 0}
        values = [float(item.get(metric_key, 0)) for item in items]
        return {
            "mean": float(np.mean(values)),
            "sigma": float(np.std(values))
        }
