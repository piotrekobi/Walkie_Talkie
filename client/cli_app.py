import curses
import threading
import time
import rest_api_func
from cli_views import GenericView


class CLIApp:
    screen: any
    tree: GenericView

    def __init__(self, tree):
        self.screen = curses.initscr()
        self.tree = tree
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def run(self):
        self.tree.show(self.screen)
        curses.endwin()


class GlobalState:
    def __init__(self):
        self.current_channel = None
        self.current_channel_name = None
        self.channels = None

    def download_channels(self):
        self.channels = rest_api_func.get_channels().json()
