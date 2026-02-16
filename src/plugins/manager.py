import os
import importlib.util
import inspect
from .base import BasePlugin
from src.logger import get_logger

logger = get_logger(__name__)

class PluginManager:
    def __init__(self, plugins_dir):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        self.conflicts = set()
        self.load_plugins()

    def load_plugins(self):
        if not os.path.exists(self.plugins_dir):
            return

        loaded_instances = {}

        for root, dirs, files in os.walk(self.plugins_dir):
            for filename in files:
                if filename.endswith(".py") and filename != "__init__.py":
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
                                    obj is not BasePlugin):
                                    plugin_instance = obj()
                                    plugin_name = plugin_instance.name
                                    
                                    if plugin_name in self.conflicts:
                                        logger.error(f"Conflict detected for plugin '{plugin_name}' at {file_path}. Plugin will not be loaded.")
                                        continue
                                    
                                    if plugin_name in loaded_instances:
                                        logger.error(f"Conflict detected: Plugin name '{plugin_name}' already exists. "
                                                     f"First found at {loaded_instances[plugin_name]._file_path}, "
                                                     f"second found at {file_path}. Refusing to load either.")
                                        self.conflicts.add(plugin_name)
                                        del loaded_instances[plugin_name]
                                        continue
                                    
                                    # Attach file path for logging purposes
                                    plugin_instance._file_path = file_path
                                    loaded_instances[plugin_name] = plugin_instance
                    except Exception as e:
                        logger.error(f"Failed to load plugin {file_path}: {e}")
        
        self.plugins = loaded_instances
