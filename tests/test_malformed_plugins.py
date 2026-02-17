import pytest
import os
from src.plugin_manager import PluginManager

def test_malformed_plugin_does_not_crash_manager(tmp_path):
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir()
    
    # 1. Syntax error
    with open(plugins_dir / "syntax_error.py", "w") as f:
        f.write("this is not python code")
    
    # 2. Logic error in initialization
    logic_error_content = """
from plugins.base import BasePlugin
class LogicErrorPlugin(BasePlugin):
    @property
    def name(self): return "Logic Error"
    @property
    def description(self): return "Error in init"
    def run(self, path): return {}
    def initialize_ui(self, main_window):
        raise RuntimeError("Boom")
"""
    with open(plugins_dir / "logic_error.py", "w") as f:
        f.write(logic_error_content)
        
    # 3. Missing abstract method
    missing_method_content = """
from plugins.base import BasePlugin
class MissingMethodPlugin(BasePlugin):
    @property
    def name(self): return "Missing Method"
    # description is missing
    def run(self, path): return {}
    def initialize_ui(self, main_window): pass
"""
    with open(plugins_dir / "missing_method.py", "w") as f:
        f.write(missing_method_content)

    # Run manager
    manager = PluginManager(str(plugins_dir))
    
    # Manager should still be alive and have 0 valid plugins (since all are malformed)
    # Actually, LogicErrorPlugin IS loaded by manager, but will fail in MainWindow
    assert "Logic Error" in manager.plugins
    assert "Missing Method" not in manager.plugins # Should fail instantiation
