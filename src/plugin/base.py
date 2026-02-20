from abc import ABC, abstractmethod
from typing import TypedDict, List, Union, Literal, Optional, Any, Dict

class PluginParameter(TypedDict):
    """Defines a single configurable parameter for a plugin."""
    name: str
    label: str
    type: Literal["int", "float", "str", "choice", "bool"]
    default: Any
    options: Optional[List[str]]  # Only for type="choice"
    min: Optional[Union[int, float]]  # For int/float
    max: Optional[Union[int, float]]  # For int/float

class PluginSchema(TypedDict):
    """Defines the full parameter schema for a plugin."""
    parameters: List[PluginParameter]

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

    @property
    def category(self) -> str:
        """Return the category of the plugin (e.g., 'sort', 'group', 'filter', 'general').

        Returns:
            str: The plugin category. Defaults to 'general'.
        """
        return "general"

    @property
    def schema(self) -> PluginSchema:
        """Returns the parameter schema for this plugin. 
        Override to provide configurable settings in the UI.

        Returns:
            PluginSchema: A dictionary defining configurable parameters.
        """
        return {"parameters": []}

    @abstractmethod
    def run(self, image_path: str) -> dict:
        """Execute the analysis on the given image.

        Args:
            image_path (str): The absolute path to the image file to analyze.

        Returns:
            dict: A dictionary of results containing metric keys and values.
        """
        pass

class SortPlugin(BasePlugin):
    """Base class for sorting plugins."""
    @property
    def category(self) -> str:
        return "sort"

    @abstractmethod
    def sort(self, items: List[Dict[str, Any]], metric_key: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Sorts the provided items based on the specified metric and parameters."""
        pass

class GroupPlugin(BasePlugin):
    """Base class for grouping plugins."""
    @property
    def category(self) -> str:
        return "group"

    @abstractmethod
    def group(self, items: List[Dict[str, Any]], metric_key: str, params: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
        """Groups the provided items based on the specified metric and parameters."""
        pass

class FilterPlugin(BasePlugin):
    """Base class for filtering plugins."""
    @property
    def category(self) -> str:
        return "filter"

    @abstractmethod
    def filter(self, items: List[Dict[str, Any]], params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filters the provided items based on the specified parameters."""
        pass
