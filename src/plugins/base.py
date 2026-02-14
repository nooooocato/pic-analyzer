from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the display name of the plugin."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of what the plugin does."""
        pass

    @abstractmethod
    def run(self, image_path: str) -> dict:
        """
        Execute the analysis on the given image.
        Returns a dictionary of results.
        """
        pass
