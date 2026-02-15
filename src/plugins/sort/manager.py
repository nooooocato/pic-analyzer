import os
import importlib.util
import inspect
from typing import Dict
from src.plugins.sort.base import BaseSortPlugin

class SortPluginManager:
    """
    Manages loading and discovery of sorting plugins.
    """
    def __init__(self, plugins_dir: str = None):
        if plugins_dir is None:
            # Default to the directory where this file resides + /sort/
            # but wait, this file is IN src/plugins/sort/
            plugins_dir = os.path.dirname(__file__)
            
        self.plugins_dir = plugins_dir
        self.plugins: Dict[str, BaseSortPlugin] = {}
        self.load_plugins()

    def load_plugins(self):
        """
        Dynamically loads sorting plugins from the specified directory.
        """
        if not os.path.exists(self.plugins_dir):
            return

        for filename in os.listdir(self.plugins_dir):
            if filename.endswith(".py") and filename not in ("__init__.py", "base.py", "manager.py"):
                module_name = filename[:-3]
                file_path = os.path.join(self.plugins_dir, filename)
                
                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)
                        
                        for name, obj in inspect.getmembers(module):
                            if (inspect.isclass(obj) and 
                                issubclass(obj, BaseSortPlugin) and 
                                obj is not BaseSortPlugin):
                                plugin_instance = obj()
                                self.plugins[plugin_instance.name] = plugin_instance
                except Exception as e:
                    print(f"Failed to load sorting plugin {filename}: {e}")

    def get_plugin(self, name: str) -> BaseSortPlugin:
        return self.plugins.get(name)
