def get_style():
    return """
        QScrollArea {
            border: none;
            background: transparent;
        }
        QSplitter::handle {
            background-color: #3d3d3d;
            height: 1px;
            margin: 0;
        }
        QSplitter::handle:hover {
            background-color: #555;
        }
        
        /* PluginItemWrapper Styling */
        QFrame#PluginItemWrapper {
            border: 1px solid #444;
            border-radius: 2px;
            background-color: #2b2b2b;
            margin: 1px;
        }
        
        QLabel#PluginItemTitle {
            font-size: 10px;
            font-weight: bold;
            color: #ccc;
        }

        QLabel#drag_handle {
            color: #666;
            font-size: 14px;
            padding: 0 2px;
        }
        
        QPushButton#remove_btn {
            background: transparent;
            color: #888;
            border: none;
            font-size: 12px;
            padding: 0;
            margin: 0;
        }
        QPushButton#remove_btn:hover {
            color: #f44;
        }
        
        /* Sidebar Add buttons */
        QPushButton {
            padding: 2px 4px;
            font-size: 10px;
            margin: 2px;
        }
        
        /* Section Header button - indicator support */
        CollapsibleSection QPushButton {
            font-weight: bold;
            font-size: 11px;
            padding: 4px;
            background-color: #333;
            border: 1px solid #222;
            text-align: left;
            border-radius: 0;
        }

        /* Gallery Title styling fix */
        QLabel#GroupHeader {
            font-weight: bold;
            font-size: 11px;
            color: #ccc;
            padding: 0 8px;
            background-color: #222;
            border-bottom: 1px solid #333;
            max-height: 22px;
            min-height: 22px;
        }

        /* Connector Styling */
        QComboBox[is_connector="true"] {
            font-size: 10px;
            padding: 1px;
        }
    """
