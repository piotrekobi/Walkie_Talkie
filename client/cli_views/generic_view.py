import curses


class GenericView:
    title: str
    screen: any
    running: bool

    def __init__(
            self,
            title,
            global_state,
            bottom_text="  Aby cofnąć do poprzedniego ekranu wciśnij 'q'"):
        self.title = title
        self.bottom_text = bottom_text
        self.running = False
        self.global_state = global_state

    def show(self, screen):
        self.running = True
        self.screen = screen

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
        if char_code == ord('q'):
            self.running = False