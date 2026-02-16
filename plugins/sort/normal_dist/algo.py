import numpy as np
from typing import List, Dict, Any

class NormalDistributionSort:
    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        if not items:
            return []
        values = [float(item.get(metric_key, 0)) for item in items]
        mean = np.mean(values)
        return sorted(items, key=lambda x: abs(float(x.get(metric_key, 0)) - mean))

    def get_stats(self, items: List[Dict[str, Any]], metric_key: str) -> Dict[str, Any]:
        if not items:
            return {"mean": 0, "sigma": 0}
        values = [float(item.get(metric_key, 0)) for item in items]
        return {
            "mean": float(np.mean(values)),
            "sigma": float(np.std(values))
        }
