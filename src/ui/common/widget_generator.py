from PySide6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QComboBox, QCheckBox, QHBoxLayout, QLabel
from typing import Any, Dict

class WidgetGenerator:
    """Factory to create PySide6 widgets from PluginParameter definitions."""

    @staticmethod
    def create_widget(param: Dict[str, Any]) -> QWidget:
        """Creates a widget for the given parameter definition."""
        p_type = param.get("type")
        default = param.get("default")
        
        if p_type == "int":
            w = QSpinBox()
            if "min" in param: w.setMinimum(int(param["min"]))
            if "max" in param: w.setMaximum(int(param["max"]))
            if default is not None: w.setValue(int(default))
            return w
            
        elif p_type == "float":
            w = QDoubleSpinBox()
            if "min" in param: w.setMinimum(float(param["min"]))
            if "max" in param: w.setMaximum(float(param["max"]))
            if default is not None: w.setValue(float(default))
            return w
            
        elif p_type == "str":
            w = QLineEdit()
            if default is not None: w.setText(str(default))
            return w
            
        elif p_type == "choice":
            w = QComboBox()
            options = param.get("options", [])
            w.addItems([str(o) for o in options])
            if default is not None:
                w.setCurrentText(str(default))
            return w
            
        elif p_type == "bool":
            w = QCheckBox()
            if default is not None:
                w.setChecked(bool(default))
            return w
            
        return QLabel(f"Unknown type: {p_type}")

    @staticmethod
    def create_labeled_widget(param: Dict[str, Any]) -> QWidget:
        """Creates a widget with a label prefix in a horizontal layout."""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(param.get("label", param.get("name", "")))
        widget = WidgetGenerator.create_widget(param)
        
        layout.addWidget(label)
        layout.addWidget(widget)
        
        # Attach name and the actual input widget to the container for easy access
        container.param_name = param["name"]
        container.input_widget = widget
        return container
