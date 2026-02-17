import sys
import os
from src.plugin.manager import PluginManager

def test_plugins_dir_in_sys_path():
    plugins_dir = "plugins"
    abs_plugins_path = os.path.abspath(plugins_dir)
    
    # Ensure it's NOT there first (if possible, though other tests might have added it)
    # assert abs_plugins_path not in sys.path 
    
    manager = PluginManager(plugins_dir)
    assert abs_plugins_path in sys.path
