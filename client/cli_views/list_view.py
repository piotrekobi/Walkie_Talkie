import curses
from cli_views.generic_view import GenericView


class ListView(GenericView):
    def __init__(
        self,
        title,
        top_text,
        global_state,
        bottom_text=" Aby wybrać kanał wciśnij ENTER. Aby cofnąć do poprzedniego ekranu wciśnij 'q'"
    ):

        super().__init__(title, global_state, bottom_text=bottom_text)
        self.top_text = top_text
        self.cursor_pos = [0, 0]

    def show(self, screen):
        self.running = True
        self.screen = screen
        channels = self.global_state.channels
        self.item_list = [
            f"{channel['id']}: {channel['name']}" for channel in channels
        ]

        while self.running:
            self.set_max_y_x()
            self.set_cursor_max()
            self.draw()
            self.event_loop()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)
        try:
            self.screen.addstr(1, 1, self.top_text, curses.A_STANDOUT)

            for i, item in enumerate(self.item_list):
                x_pos = 10 * (i // self.max_y) + 1
                y_pos = (i % (self.max_y)) + 2
                style = curses.A_NORMAL
                if self.cursor_pos == [(i // self.max_y), (i % self.max_y)]:
                    style = curses.A_STANDOUT
                self.screen.addstr(y_pos, x_pos, item, style)

            self.screen.addstr(
                self.max_y + 1, 0, self.bottom_text + ' ' *
                (self.max_x - 1 - len(self.bottom_text)), curses.A_STANDOUT)
            try:
                self.screen.addch(self.max_y + 1, self.max_x - 1, ' ',
                                  curses.A_STANDOUT)
            except curses.error:
                pass
        except curses.error:
            pass

    def event_loop(self):
        char_code = self.screen.getch()

        if char_code == ord('q'):
            self.running = False

        if char_code == curses.KEY_UP:
            self.cursor_pos[1] = (self.cursor_pos[1] -
                                  1) % self.current_cursor_max_height

        if char_code == curses.KEY_DOWN:
            self.cursor_pos[1] = (self.cursor_pos[1] +
                                  1) % self.current_cursor_max_height

        if char_code == curses.KEY_LEFT:
            self.cursor_pos[0] = (self.cursor_pos[0] -
                                  1) % self.current_cursor_max_width

        if char_code == curses.KEY_RIGHT:
            self.cursor_pos[0] = (self.cursor_pos[0] +
                                  1) % self.current_cursor_max_width

        if char_code == 10 or char_code == curses.KEY_ENTER:
            self.set_choice()
            self.running = False

    def set_max_y_x(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.max_y -= 2

    def set_cursor_max(self):

        last_column_length = len(self.item_list) % self.max_y
        self.current_cursor_max_width = len(self.item_list) // self.max_y
        if (last_column_length > self.cursor_pos[1]):
            self.current_cursor_max_width += 1

        self.current_cursor_max_height = self.max_y - 1
        if self.cursor_pos[0] == (len(self.item_list) // self.max_y):
            self.current_cursor_max_height = last_column_length

    def set_choice(self):
        index = (self.max_y * self.cursor_pos[0] + self.cursor_pos[1])
        self.global_state.current_channel_name = self.item_list[index]
        self.global_state.current_channel = self.global_state.channels[index]
