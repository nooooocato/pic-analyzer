# **PySide6 Modular Python Style Guide**

This document outlines the **"Triple-Python Pattern"**, a strict architectural style that maintains the separation of concerns (like Web dev) while keeping everything in pure Python (like Engineering dev).

## **1. General Philosophy**

* **Pure Python:** No .ui or external .qss files.  
* **Strict Separation:** Every component is split into three specific Python files based on responsibility.  
* **Composition/Inheritance:** The Logic layer inherits or composes the Layout layer, which applies the Style layer.

## **2. File Naming & Structure**

For a component named LoginPanel, you must create three files:

1. **login_panel.style.py** (The Skin)  
   * Contains configuration dictionaries, colors, fonts, and QSS strings.  
   * *Analogy:* CSS / Tailwind Config.  
2. **login_panel.layout.py** (The Skeleton)  
   * Defines the QtWidget subclass.  
   * Initializes widgets and layouts.  
   * **Rule:** No business logic allowed here.  
   * *Analogy:* HTML DOM structure.  
3. **login_panel.logic.py** (The Brain)  
   * The entry point class.  
   * Connects signals to slots.  
   * Handles data processing.  
   * *Analogy:* JavaScript / React Component Logic.

## **3. Detailed Responsibilities**

### **A. The Style File (xxx.style.py)**

Define styles as Python constants or functions. This allows dynamic theming (e.g., changing colors based on OS settings).
```python
# login_panel.style.py

# Constants for reuse  
PRIMARY_COLOR = "#007AFF"  
ERROR_COLOR = "#FF3B30"

# Component-specific stylesheet  
LOGIN_PANEL_QSS = f"""  
    QFrame#login_frame {{  
        background-color: white;  
        border-radius: 8px;  
    }}  
    QPushButton {{  
        background-color: {PRIMARY_COLOR};  
        color: white;  
    }}  
"""

def get_error_style():  
    return f"color: {ERROR_COLOR}; font-weight: bold;"
```
### **B. The Layout File (xxx.layout.py)**

Focus purely on hierarchy. Use type hinting for all widgets so the Logic layer has full Intellisense support.
```python
# login_panel.layout.py  
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel  
from .login_panel_style import LOGIN_PANEL_QSS

class LoginPanelLayout(QWidget):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self._init_ui()  
        self._apply_style()

    def _init_ui(self):  
        # 1. Create Layout  
        self.main_layout = QVBoxLayout(self)

        # 2. Create Widgets (Public for Logic layer)  
        self.user_input = QLineEdit()  
        self.user_input.setPlaceholderText("Username")  
          
        self.pass_input = QLineEdit()  
        self.pass_input.setPlaceholderText("Password")  
        self.pass_input.setEchoMode(QLineEdit.Password)  
          
        self.submit_btn = QPushButton("Login")  
        self.error_lbl = QLabel("")

        # 3. Assemble  
        self.main_layout.addWidget(self.user_input)  
        self.main_layout.addWidget(self.pass_input)  
        self.main_layout.addWidget(self.error_lbl)  
        self.main_layout.addWidget(self.submit_btn)

    def _apply_style(self):  
        # Apply the style from the style.py file  
        self.setStyleSheet(LOGIN_PANEL_QSS)
```
### **C. The Logic File (xxx.logic.py)**

This is the only class the rest of the application should import.
```python
# login_panel.logic.py  
from PySide6.QtCore import Slot  
from .login_panel_layout import LoginPanelLayout  
from .login_panel_style import get_error_style

class LoginPanel(LoginPanelLayout):  
    def __init__(self, parent=None):  
        super().__init__(parent)  
        self._connect_signals()

    def _connect_signals(self):  
        # Access widgets defined in the Layout parent class  
        self.submit_btn.clicked.connect(self._on_login_clicked)

    @Slot()  
    def _on_login_clicked(self):  
        username = self.user_input.text()  
        password = self.pass_input.text()

        if not username or not password:  
            self._show_error("Fields cannot be empty")  
            return  
          
        print(f"Logging in {username}...")

    def _show_error(self, message):  
        self.error_lbl.setText(message)  
        # Dynamic style injection from style.py  
        self.error_lbl.setStyleSheet(get_error_style())
```
## **4. Workflow Rules**

1. **Start with Style:** Define your visual variables in xxx.style.py.  
2. **Build the View:** Create the widgets in xxx.layout.py. Don't worry about what they do, just where they are.  
3. **Implement Logic:** Create xxx.logic.py, inherit the Layout, and breathe life into it.

## **5. Benefits of Triple-Python**

| Feature | .ui \+ .qss | Single .py | Triple-Python |
| :---- | :---- | :---- | :---- |
| **Separation** | Excellent | Poor | **Excellent** |
| **Dynamic Styles** | Hard | Easy | **Easy** |
| **IDE Support** | Poor | Excellent | **Excellent** |
| **Refactoring** | Risky | Safe | **Safe** |

**Recommendation:** Use this pattern for teams that want the cleanliness of MVC/Web patterns but demand the robustness of Python.

## **6. Adapted Rules from HTML/CSS Guide**

### **A. Semantics & Widget Choice (The HTML Analogy)**

Just as HTML requires \<button\> for actions and \<a\> for links, PySide requires the correct widget type.

* **Rule:** Do not mock widgets using generic containers plus click events.  
  * **Bad:** Using a QLabel with a mousePressEvent to simulate a button.  
  * **Good:** Use QPushButton or QToolButton and style it flat if necessary.  
* **Rule:** Use specific inputs over generic ones.  
  * **Bad:** QLineEdit for numbers.  
  * **Good:** QSpinBox or QDoubleSpinBox.

### **B. Dynamic Classes via Properties (The CSS Analogy)**

The HTML guide says: *"Avoid ID selectors for styling. Prefer class selectors."*

In PySide6, setObjectName is the ID. To simulate **CSS Classes**, use **Dynamic Properties**.

2. **Concept:** Instead of creating a unique ID for every red button, mark them with a property.  
3. **In xxx.layout.py:**
```python  
self.delete_btn.setProperty("class", "danger") # Simulates <button class="danger">  
self.save_btn.setProperty("class", "primary")  # Simulates <button class="primary">
```
4. **In xxx.style.py:**  
```python  
# Target the property, not the specific widget instance
COMMON_STYLE = """  
    QPushButton[class="danger"] { background-color: #ff4444; }  
    QPushButton[class="primary"] { background-color: #007bff; }  
"""
```
### **C. Accessibility & Fallbacks (The Alt-Text Analogy)**

The HTML guide says: *"Provide alt text for images."*

In PySide6, this translates to Tooltips and Accessible Names for screen readers.

2. **Rule:** Every interactive element with an icon but no text *must* have a tooltip.  
3. **In xxx.layout.py:**
```python  
self.help_btn = QPushButton()  
self.help_btn.setIcon(QIcon(":/icons/help.png"))  
# MANDATORY for icon-only buttons:  
self.help_btn.setToolTip("Open Help Documentation")  
self.help_btn.setAccessibleName("Help Button")
```
### **D. Formatting Embedded QSS (The CSS Formatting Analogy)**

Since we are embedding CSS strings inside Python files (xxx.style.py), formatting is critical to avoid "Spaghetti String" code.

4. **Rule:** Use Python's triple-quotes """ and indentation to match the CSS guide.  
5. **Rule:** Alphabetize properties within the string.  
6. **Bad:**  
   BTN_STYLE = "color:red;background:black;border:none;"

7. **Good:**
```python  
BTN_STYLE = """  
QPushButton {  
    background-color: black;  
    border: none;  
    color: red;  
    padding: 5px;  
}  
"""
```
### **E. Protocol & Resources**

The HTML guide says: *"Use HTTPS for embedded resources."*

In PySide6, strict resource management prevents file-not-found errors.

* **Rule:** Never use absolute file paths (e.g., C:/Users/.../img.png).  
* **Rule:** Always use the Qt Resource System (:/prefix/path) for stability, or strictly relative paths handled by a helper function in style.py.