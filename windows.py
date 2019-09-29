try:
    import win32gui
    import re

    class WindowMgr:
        """Encapsulates some calls to the winapi for window management"""

        def __init__ (self):
            """Constructor"""
            self._handle = None

        def find_window(self, class_name, window_name=None):
            """find a window by its class_name"""
            self._handle = win32gui.FindWindow(class_name, window_name)

        def _window_enum_callback(self, hwnd, wildcard):
            """Pass to win32gui.EnumWindows() to check all the opened windows"""
            if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
                self._handle = hwnd

        def find_window_wildcard(self, wildcard):
            """find a window whose title matches the wildcard regex"""
            self._handle = None
            win32gui.EnumWindows(self._window_enum_callback, wildcard)

        def set_foreground(self):
            """put the window in the foreground"""
            win32gui.SetForegroundWindow(self._handle)

    def select_window(title_regex):
        w = WindowMgr()
        w.find_window_wildcard(title_regex)
        w.set_foreground()

except ImportError:
    print("WARNING: Window utilities like SELECT_WINDOW are currently only implemented for Windows operating systems. These commands will not work on your system. :(")

    def select_window(title_regex):
        # Do nothing (not implemented for Linux yet)
        w = 0
