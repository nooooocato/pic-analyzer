from qfluentwidgets import CommandBar, Action, FluentIcon

class SortOverlayLayout:
    def setup_ui(self, widget: CommandBar):
        """Sets up the UI. 'widget' is expected to be a CommandBar."""
        # Add Sort action
        self.sort_action = Action(FluentIcon.FILTER, 'Sort Options', widget)
        widget.addAction(self.sort_action)
        
        # In CommandBar, we don't have a 'btn_sort' button directly accessible 
        # like before, but we can access the widget created for the action 
        # if needed. However, it's better to use the Action's menu.
        return self.sort_action
