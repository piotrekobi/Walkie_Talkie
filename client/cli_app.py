import curses
import threading
import time
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

        # threading.Thread(target=self.key_events_thread, daemon=True)
        # threading.Thread(target=self.time_events_thread, daemon=True)

    def run(self):
        self.tree.show(self.screen)
        curses.endwin()

    # def key_events_thread(self):
    #     while True:
    #         char_code = self.screen.getch()

    # def time_events_thread(self):
    #     while True:
    #         time.sleep(0.5)


class GlobalState:
    def __init__(self):
        self.current_channel = None
