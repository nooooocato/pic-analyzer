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
    """Abstract base class for all plugins in the Pic-Analyzer system."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    def category(self) -> str:
        return "general"

    @property
    def schema(self) -> PluginSchema:
        """Returns the parameter schema for this plugin. 
        Override to provide configurable settings in the UI.
        """
        return {"parameters": []}

    @abstractmethod
    def run(self, image_path: str) -> dict:
        pass

    def initialize_ui(self, main_window) -> None:
        """DEPRECATED: Use schema and logic-only methods instead."""
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
