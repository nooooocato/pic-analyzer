from abc import ABC, abstractmethod

class BasePlugin(ABC):
    """Abstract base class for all plugins in the Pic-Analyzer system.

    Plugins must implement this interface to be discovered and loaded by the
    PluginManager.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the display name of the plugin.

        Returns:
            str: The name of the plugin as it should appear in the UI.
        """
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a brief description of what the plugin does.

        Returns:
            str: A short description of the plugin's functionality.
        """
        pass

    @abstractmethod
    def run(self, image_path: str) -> dict:
        """Execute the analysis on the given image.

        Args:
            image_path (str): The absolute path to the image file to analyze.

        Returns:
            dict: A dictionary of results containing metric keys and values.
        """
        pass

    @abstractmethod
    def initialize_ui(self, main_window) -> None:
        """Initialize the plugin's UI components.

        This method is called during application startup. Plugins should use
        this to register themselves with the MainWindow's UI components
        (e.g., adding menu items, toolbar buttons, or sorting algorithms).

        Args:
            main_window: A reference to the MainWindow instance.
        """
        pass
