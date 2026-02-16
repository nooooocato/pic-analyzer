from src.plugins.base import *


class p1(BasePlugin):
    @property
    def name(self) -> str:
        return "ConflictPlugin"

    @property
    def description(self) -> str:
        return "Groups images by their modification date (YYYY-MM-DD)."

    def run(self, image_path: str, granularity: str = "month") -> dict:
        pass
    