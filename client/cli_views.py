import curses
import curses.textpad
import time
from call_controler import CallController
from config.server import SERVER_URL, MIC_PORT, SPEAKER_PORT, USER_ID


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
        self.start_time = time.time()
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
        self.global_state.current_channel = self.item_list[index]


class CallView(GenericView):
    def __init__(self,
                 title,
                 global_state,
                 bottom_text=' Aby rozłączyć się, wciśnij "q"'):
        super().__init__(title, global_state, bottom_text=bottom_text)

        self.call_controller = CallController(url=SERVER_URL,
                                              mic_port=MIC_PORT,
                                              speaker_port=SPEAKER_PORT,
                                              user_id=USER_ID)

    def show(self, screen):
        self.running = True
        self.screen = screen
        curses.halfdelay(10)

        self.call_controller.connect(
            int(self.global_state.current_channel.split(':')[0]))

        while self.running:
            self.draw()
            self.event_loop()

        self.call_controller.disconnect()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()
        channel_info = self.global_state.current_channel

        if channel_info is None:
            no_channel_chosen_text = "Brak wybranego kanału"
            self.screen.addstr(1, (x - len(no_channel_chosen_text)) // 2,
                               no_channel_chosen_text, curses.A_STANDOUT)
        else:
            self.top_text = f"Rozmowa na kanale {channel_info}"
            self.screen.addstr(1, (x - len(self.top_text)) // 2, self.top_text,
                               curses.A_STANDOUT)

            call_time = round(time.time() - self.start_time)
            minutes, seconds = divmod(call_time, 60)
            time_text = f"Czas rozmowy: {minutes:02d}:{seconds:02d}"
            self.screen.addstr(3, (x - len(time_text)) // 2, time_text,
                               curses.A_NORMAL)

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


class SelectView(GenericView):
    def __init__(self,
                 title,
                 global_state,
                 options,
                 top_text,
                 bottom_text="  Aby opuścić aplikację wciśnij 'q'"):
        super().__init__(title, global_state, bottom_text)
        self.options = options
        self.cursor_pos = 0
        self.top_text = top_text
        self.current_channel_id = "Brak"

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        self.screen.addstr(1, (x - len(self.title)) // 2, self.title,
                           curses.A_STANDOUT)

        self.screen.addstr(2, 3, self.top_text, curses.A_NORMAL)

        self.screen.addstr(2, 4 + len(self.top_text), self.current_channel_id,
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

    def set_current_channel_id(self):
        if self.global_state.current_channel is not None:
            self.current_channel_id = self.global_state.current_channel

    def event_loop(self):
        char_code = self.screen.getch()

        if char_code == ord('q'):
            self.running = False

        if char_code == curses.KEY_UP:
            self.cursor_pos = (self.cursor_pos - 1) % len(self.options)

        if char_code == curses.KEY_DOWN:
            self.cursor_pos = (self.cursor_pos + 1) % len(self.options)

        if char_code == 10 or char_code == curses.KEY_ENTER:
            self.global_state.download_channels()
            self.options[self.cursor_pos].start_time = time.time()
            self.options[self.cursor_pos].show(self.screen)

        self.set_current_channel_id()


class PasswordView(GenericView):
    def __init__(
            self,
            title,
            global_state,
            top_text,
            bottom_text="  Aby cofnąć do poprzedniego ekranu wciśnij 'q'"):
        super().__init__(title, global_state, bottom_text=bottom_text)
        self.cursor_pos = [0, 0]
        self.password = [None, None, None, None]
        self.current_index = 0
        self.top_text = top_text
        self.keyboard_buttons = [str(i) for i in range(1, 10)]
        self.keyboard_buttons.append("0")

    def show(self, screen):
        self.running = True
        self.screen = screen

        while self.running:
            self.set_max_y_x()
            self.set_cursor_max()
            self.draw()
            self.event_loop()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()
        rectangle_x, rectangle_y = (x // 2) - 6, 2

        self.screen.addstr(1, rectangle_x, self.top_text, curses.A_NORMAL)

        curses.textpad.rectangle(self.screen, rectangle_y, rectangle_x,
                                 rectangle_y + 2, rectangle_x + 12)

        for i, num in enumerate(self.password):
            if num is not None:
                self.screen.addstr(3, rectangle_x + 1 + i * 3, num,
                                   curses.A_NORMAL)

        first_button_x_pos = (x // 2) - 4
        for i, button in enumerate(self.keyboard_buttons):
            style = curses.A_NORMAL
            if self.cursor_pos == [(i % 3), (i // 3)]:
                style = curses.A_STANDOUT

            x_pos = first_button_x_pos + (4 * (i % 3))
            y_pos = 5 + (2 * (i // 3))
            if i == 9:
                x_pos += 4
                if self.cursor_pos == [1, 3]:
                    style = curses.A_STANDOUT
            self.screen.addstr(y_pos, x_pos, button, style)

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

        if char_code == curses.KEY_UP:
            self.cursor_pos[1] = (self.cursor_pos[1] -
                                  1) % self.current_cursor_max_height

        if char_code == curses.KEY_DOWN:
            self.cursor_pos[1] = (self.cursor_pos[1] +
                                  1) % self.current_cursor_max_height

        if char_code == curses.KEY_LEFT:
            if self.cursor_pos != [1, 3]:
                self.cursor_pos[0] = (self.cursor_pos[0] -
                                      1) % self.current_cursor_max_width

        if char_code == curses.KEY_RIGHT:
            if self.cursor_pos != [1, 3]:
                self.cursor_pos[0] = (self.cursor_pos[0] +
                                      1) % self.current_cursor_max_width

        if char_code == 10 or char_code == curses.KEY_ENTER:
            self.set_password_num()

        # char_code = "delete"
        if char_code == 127 or char_code == curses.KEY_BACKSPACE:
            self.delete_password_num()

    def set_max_y_x(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.max_y -= 2

    def set_password_num(self):
        if self.current_index < 4:
            if self.cursor_pos == [1, 3]:
                number = "0"
            else:
                number = self.keyboard_buttons[self.cursor_pos[0] +
                                               self.cursor_pos[1] * 3]

            self.password[self.current_index] = number
            self.current_index = min(4, self.current_index + 1)

    def delete_password_num(self):

        self.current_index = max(0, self.current_index - 1)
        self.password[self.current_index] = None

    def set_cursor_max(self):
        self.current_cursor_max_width = 3

        self.current_cursor_max_height = 3
        if self.cursor_pos[0] == 1:
            self.current_cursor_max_height = 4
