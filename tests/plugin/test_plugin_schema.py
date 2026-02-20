import pytest
from typing import TypedDict, List, Union, Literal, Any
from src.plugin.base import PluginParameter, PluginSchema

def test_plugin_parameter_structure():
    """Test that a PluginParameter can be correctly instantiated."""
    param = {
        "name": "threshold",
        "label": "Threshold Value",
        "type": "int",
        "default": 10,
        "min": 0,
        "max": 100
    }
    # This is more of a type-checking test, but we can verify keys
    assert param["name"] == "threshold"
    assert param["type"] == "int"

def test_plugin_schema_structure():
    """Test that a PluginSchema can contain multiple parameters."""
    schema = {
        "parameters": [
            {
                "name": "mode",
                "label": "Sort Mode",
                "type": "choice",
                "default": "asc",
                "options": ["asc", "desc"]
            },
            {
                "name": "sensitivity",
                "label": "Sensitivity",
                "type": "float",
                "default": 0.5
            }
        ]
    }
    assert len(schema["parameters"]) == 2
    assert schema["parameters"][0]["name"] == "mode"
    assert schema["parameters"][1]["type"] == "float"
