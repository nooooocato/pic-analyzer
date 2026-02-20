import pytest
from PySide6.QtWidgets import QSpinBox, QComboBox, QLineEdit, QCheckBox
from src.ui.common.widget_generator import WidgetGenerator

def test_generate_int_widget(qtbot):
    """Test generating a widget for an integer parameter."""
    param = {"name": "p1", "type": "int", "default": 5, "label": "P1", "min": 0, "max": 10}
    widget = WidgetGenerator.create_widget(param)
    qtbot.addWidget(widget)
    
    assert isinstance(widget, QSpinBox)
    assert widget.value() == 5
    assert widget.minimum() == 0
    assert widget.maximum() == 10

def test_generate_choice_widget(qtbot):
    """Test generating a widget for a choice parameter."""
    param = {"name": "p2", "type": "choice", "default": "b", "label": "P2", "options": ["a", "b", "c"]}
    widget = WidgetGenerator.create_widget(param)
    qtbot.addWidget(widget)
    
    assert isinstance(widget, QComboBox)
    assert widget.currentText() == "b"
    assert widget.count() == 3

def test_generate_bool_widget(qtbot):
    """Test generating a widget for a boolean parameter."""
    param = {"name": "p3", "type": "bool", "default": True, "label": "P3"}
    widget = WidgetGenerator.create_widget(param)
    qtbot.addWidget(widget)
    
    assert isinstance(widget, QCheckBox)
    assert widget.isChecked() is True
