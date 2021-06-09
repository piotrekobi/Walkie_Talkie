import curses
import threading
import time


class EventBus:
    def emit(self, event):
        pass

    def subscribe(self, event_name, callback):
        pass


class Event:
    def __init__(self, name, data):
        pass


class GenericView:
    title: str
    screen: any
    running: bool
    event_bus: EventBus

    def __init__(
            self,
            title,
            bottom_text="  Aby cofnąć do poprzedniego ekranu wciśnij 'q'"):
        self.title = title
        self.bottom_text = bottom_text
        self.running = False

    def show(self, screen, event_bus=None):
        self.running = True
        self.screen = screen
        self.event_bus = event_bus

        while self.running:
            self.draw()
            self.event_loop()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        self.screen.addstr(1, (x - len(self.title)) // 2, self.title,
                           curses.A_STANDOUT)

        self.screen.addstr(
            y - 1, 0, self.bottom_text + ' ' * (x - 1 - len(self.bottom_text)),
            curses.A_STANDOUT)
        try:
            self.screen.addch(y - 1, x - 1, ' ', curses.A_STANDOUT)
        except curses.error:
            pass

    def event_loop(self):
        char_code = self.screen.getch()
        # char_code == 'q'
        if char_code == 113:
            self.running = False


class ListView(GenericView):
    def __init__(self,
                 title,
                 top_text,
                 item_list,
                 bottom_text=" Aby cofnąć do poprzedniego ekranu wciśnij 'q'"):

        super().__init__(title, bottom_text=bottom_text)
        self.top_text = top_text
        self.item_list = item_list

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        self.screen.addstr(1, (x - len(self.title)) // 2, self.top_text,
                           curses.A_STANDOUT)

        for i, item in enumerate(self.item_list):
            x_pos = 10 * (i // 5) + 1
            y_pos = 2 + (i % 5)
            self.screen.addstr(y_pos, x_pos, item, curses.A_NORMAL)

        self.screen.addstr(
            y - 1, 0, self.bottom_text + ' ' * (x - 1 - len(self.bottom_text)),
            curses.A_STANDOUT)
        try:
            self.screen.addch(y - 1, x - 1, ' ', curses.A_STANDOUT)
        except curses.error:
            pass


class SelectView(GenericView):
    def __init__(self,
                 title,
                 options,
                 bottom_text="  Aby opuścić aplikację wciśnij 'q'"):
        super().__init__(title, bottom_text)
        self.options = options

        self.cursor_pos = 0

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        self.screen.addstr(1, (x - len(self.title)) // 2, self.title,
                           curses.A_STANDOUT)

        pos = 4
        for i in range(len(self.options)):
            style = curses.A_NORMAL

            if i == self.cursor_pos:
                style = curses.A_STANDOUT

            self.screen.addstr(pos, 3, self.options[i].title, style)
            pos += 1

        self.screen.addstr(
            y - 1, 0, self.bottom_text + ' ' * (x - 1 - len(self.bottom_text)),
            curses.A_STANDOUT)
        try:
            self.screen.addch(y - 1, x - 1, ' ', curses.A_STANDOUT)
        except curses.error:
            pass

    def event_loop(self):
        char_code = self.screen.getch()

        # char_code == 'q'
        if char_code == 113:
            self.running = False

        if char_code == curses.KEY_UP:
            self.cursor_pos = (self.cursor_pos - 1) % len(self.options)

        if char_code == curses.KEY_DOWN:
            self.cursor_pos = (self.cursor_pos + 1) % len(self.options)

        if char_code == 10 or char_code == curses.KEY_ENTER:
            self.options[self.cursor_pos].show(self.screen)


class CallView(GenericView):
    pass


class CLIApp:
    screen: any
    tree: GenericView
    event_bus: EventBus

    def __init__(self, tree):
        self.screen = curses.initscr()
        self.tree = tree
        self.event_bus = EventBus()
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        self.screen.keypad(1)

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        threading.Thread(target=self.key_events_thread, daemon=True)
        threading.Thread(target=self.time_events_thread, daemon=True)

    def run(self):
        self.tree.show(self.screen, self.event_bus)
        curses.endwin()

    def key_events_thread(self):
        while True:
            char_code = self.screen.getch()
            self.event_bus.emit(Event('keypress', char_code))

    def time_events_thread(self):
        while True:
            time.sleep(0.5)
            self.event_bus.emit(Event('update', None))
