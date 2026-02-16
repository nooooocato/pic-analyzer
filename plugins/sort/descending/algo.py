from typing import List, Dict, Any

class DescendingSort:
    def sort(self, items: List[Dict[str, Any]], metric_key: str) -> List[Dict[str, Any]]:
        return sorted(items, key=lambda x: x.get(metric_key, 0), reverse=True)
