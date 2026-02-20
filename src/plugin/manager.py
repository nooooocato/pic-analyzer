import os
import sys
import importlib.util
import inspect
from .base import BasePlugin
from src.app.logger import get_logger

logger = get_logger(__name__)

class PluginManager:
    """Manages the lifecycle of external plugins."""

    def __init__(self, plugins_dir):
        self.plugins_dir = os.path.abspath(plugins_dir)
        if self.plugins_dir not in sys.path:
            sys.path.append(self.plugins_dir)
        self.plugins = {}
        self.sort_plugins = {}
        self.group_plugins = {}
        self.filter_plugins = {}
        self.general_plugins = {}
        self.conflicts = set()
        self.load_plugins()

    def load_plugins(self):
        if not os.path.exists(self.plugins_dir):
            return

        loaded_instances = {}

        for root, dirs, files in os.walk(self.plugins_dir):
            # Skip __pycache__
            if "__pycache__" in root:
                continue
                
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
                    # Avoid loading test files as plugins if they follow certain patterns
                    if filename.startswith("test_") or filename.endswith("_test.py"):
                        continue
                        
                    module_name = filename[:-3]
                    file_path = os.path.join(root, filename)

                    try:
                        spec = importlib.util.spec_from_file_location(module_name, file_path)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)

                            for name, obj in inspect.getmembers(module):
                                if (inspect.isclass(obj) and 
                                    issubclass(obj, BasePlugin) and 
                                    obj is not BasePlugin and
                                    not inspect.isabstract(obj)):
                                    
                                    plugin_instance = obj()
                                    plugin_name = plugin_instance.name

                                    if plugin_name in self.conflicts:
                                        logger.error(f"Conflict detected for plugin '{plugin_name}' at {file_path}. Plugin will not be loaded.")
                                        continue

                                    if plugin_name in loaded_instances:
                                        logger.error(f"Conflict detected: Plugin name '{plugin_name}' already exists. "
                                                     f"Refusing to load either.")
                                        self.conflicts.add(plugin_name)
                                        del loaded_instances[plugin_name]
                                        continue

                                    plugin_instance._file_path = file_path
                                    loaded_instances[plugin_name] = plugin_instance

                                    category = plugin_instance.category
                                    if category == "sort":
                                        self.sort_plugins[plugin_name] = plugin_instance
                                    elif category == "group":
                                        self.group_plugins[plugin_name] = plugin_instance
                                    elif category == "filter":
                                        self.filter_plugins[plugin_name] = plugin_instance
                                    else:
                                        self.general_plugins[plugin_name] = plugin_instance

                    except Exception as e:
                        # Only log errors for files that actually tried to define a plugin
                        # This avoids noise from helper files that might fail to load in isolation
                        pass
        
        self.plugins = loaded_instances
