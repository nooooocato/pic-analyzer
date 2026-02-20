import os
from typing import List, Dict, Any
from src.plugin.base import FilterPlugin, PluginSchema

class FileTypeFilter(FilterPlugin):
    """Filters items by their file extension."""

    @property
    def name(self) -> str:
        return "File Type"

    @property
    def description(self) -> str:
        return "Filter images by file extension."

    @property
    def schema(self) -> PluginSchema:
        return {
            "parameters": [
                {
                    "name": "extension",
                    "label": "Extension",
                    "type": "choice",
                    "default": ".jpg",
                    "options": [".jpg", ".png", ".webp", ".gif", ".bmp"]
                }
            ]
        }

    def filter(self, items: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        target_ext = params.get("extension", ".jpg").lower()
        return [item for item in items if item.get("path", "").lower().endswith(target_ext)]

    def run(self, image_path: str) -> dict:
        return {}
