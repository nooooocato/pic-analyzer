from PySide6.QtCore import QObject, Signal

class Communicator(QObject):
    """
    Centralized communication hub (Event Bus) for the application.
    Implements a singleton pattern to facilitate decoupling between components.
    """
    _instance = None
    
    # Signals
    # notify(message: str, level: str) - level can be "INFO", "WARNING", "ERROR", "SUCCESS"
    notify = Signal(str, str)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Communicator, cls).__new__(cls, *args, **kwargs)
            # Initialize QObject immediately upon creation
            super(Communicator, cls._instance).__init__()
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # Prevent re-initialization logic if already initialized
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
