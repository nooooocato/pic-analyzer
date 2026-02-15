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

        """

        Initializes the manager and loads plugins from the specified directory.

        

        Args:

            plugins_dir (str, optional): Path to the directory containing plugins.

                                         Defaults to the manager's file location.

        """

        if plugins_dir is None:

            # Default to the directory where this file resides

            plugins_dir = os.path.dirname(__file__)



        self.plugins_dir = plugins_dir

        self.plugins: Dict[str, BaseSortPlugin] = {}

        self.load_plugins()



    def load_plugins(self) -> None:

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



    def get_plugin(self, name: str) -> BaseSortPlugin | None:

        """

        Returns a plugin instance by its name.

        

        Args:

            name (str): The name of the sorting algorithm.

            

        Returns:

            BaseSortPlugin | None: The plugin instance or None if not found.

        """

        return self.plugins.get(name)


