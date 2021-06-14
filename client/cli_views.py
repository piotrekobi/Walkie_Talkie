import curses
import curses.textpad
import time
from rest_api_func import channel_connection_info, create_channel
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
        self.global_state.current_channel_name = self.item_list[index]
        self.global_state.current_channel = self.global_state.channels[index]


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
        self.user_password = None

    def show(self, screen):
        self.correct_password = False
        self.running = True
        self.screen = screen
        curses.halfdelay(10)

        self.channel_info = channel_info = self.global_state.current_channel_name
        if self.channel_info is not None:
            channel_id = self.global_state.current_channel["id"]
            self.call_controller.connect(channel_id, self.user_password)
            if channel_connection_info(channel_id,
                                       self.user_password).status_code == 200:
                self.correct_password = True
                self.user_password = None
        self.start_time = time.time()
        while self.running:
            self.draw()
            self.event_loop()

        if self.channel_info is not None:
            self.call_controller.disconnect()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        if self.channel_info is None:
            no_channel_chosen_text = "Brak wybranego kanału"
            self.screen.addstr(5, (x - len(no_channel_chosen_text)) // 2,
                               no_channel_chosen_text, curses.A_STANDOUT)

        elif self.correct_password is False:
            wrong_password_text = "Nieprawidłowe hasło"
            self.screen.addstr(5, (x - len(wrong_password_text)) // 2,
                               wrong_password_text, curses.A_STANDOUT)

        else:
            self.top_text = f"Rozmowa na kanale {self.channel_info}"
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
        if self.global_state.current_channel_name is not None:
            self.current_channel_id = self.global_state.current_channel_name

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
            if self.cursor_pos == 1 and self.global_state.current_channel is not None and self.global_state.current_channel.get(
                    "has_password"):
                PasswordView(next_screen=self.options[self.cursor_pos],
                             global_state=self.global_state,
                             top_text="Podaj hasło:").show(self.screen)
            else:
                self.options[self.cursor_pos].show(self.screen)

        self.set_current_channel_id()


class PasswordView(GenericView):
    def __init__(
            self,
            next_screen,
            global_state,
            top_text,
            title=None,
            bottom_text="  Aby cofnąć do poprzedniego ekranu wciśnij 'q'"):
        super().__init__(title, global_state, bottom_text=bottom_text)
        self.cursor_pos = [0, 0]
        self.password = [None, None, None, None]
        self.current_index = 0
        self.top_text = top_text
        self.keyboard_buttons = [str(i) for i in range(1, 10)]
        self.keyboard_buttons.append("0")
        self.next_screen = next_screen

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

        # char_code = delete
        if char_code == 127 or char_code == curses.KEY_BACKSPACE:
            self.delete_password_num()

    def set_max_y_x(self):
        self.max_y, self.max_x = self.screen.getmaxyx()
        self.max_y -= 2

    def set_password_num(self):
        if self.cursor_pos == [1, 3]:
            number = "0"
        else:
            number = self.keyboard_buttons[self.cursor_pos[0] +
                                           self.cursor_pos[1] * 3]

        self.password[self.current_index] = number
        self.current_index = min(4, self.current_index + 1)
        if self.current_index == 4:
            self.next_screen.user_password = "".join(self.password)
            self.running = False
            self.next_screen.show(self.screen)

    def delete_password_num(self):
        self.current_index = max(0, self.current_index - 1)
        self.password[self.current_index] = None

    def set_cursor_max(self):
        self.current_cursor_max_width = 3

        self.current_cursor_max_height = 3
        if self.cursor_pos[0] == 1:
            self.current_cursor_max_height = 4


class AddView(GenericView):
    def __init__(
        self,
        title,
        global_state,
        bottom_text='  q - powró† do menu;  p  - przełączenie ustawienia hasła;  u - zmiana wielkości litery;  ENTER - utworzenie kanału'
    ):
        super().__init__(title, global_state, bottom_text=bottom_text)
        self.top_text = "Dodawanie kanału"
        self.password_options = ["Nie", "Tak"]
        self.user_password = None

    def show(self, screen):
        self.running = True
        self.screen = screen

        self.input_name = ["_", "_", "_", "_", "_"]
        self.cursor_pos = 0
        self.pass_choice = 0

        if self.user_password is not None:
            self.add_channel()

        while self.running:
            self.draw()
            self.event_loop()

    def draw(self):
        self.screen.clear()
        self.screen.border(0)

        y, x = self.screen.getmaxyx()

        self.screen.addstr(1, (x - len(self.top_text)) // 2, self.top_text,
                           curses.A_STANDOUT)
        text_pos_x = x // 4
        name_prompt = "Nazwa kanału:"
        pass_prompt = "Wymagaj hasła:"
        self.screen.addstr(5, text_pos_x, name_prompt, curses.A_NORMAL)
        self.screen.addstr(7, text_pos_x, pass_prompt, curses.A_NORMAL)

        for i, char in enumerate(self.input_name):
            char_pos = text_pos_x + len(name_prompt) + 1 + 2 * i
            style = curses.A_NORMAL
            if self.cursor_pos == i:
                style = curses.A_STANDOUT
            self.screen.addstr(5, char_pos, char, style)

        pass_pos = text_pos_x + len(pass_prompt) + 1
        self.screen.addstr(7, pass_pos,
                           self.password_options[self.pass_choice],
                           curses.A_STANDOUT)

        self.screen.addstr(
            y - 1, 0, self.bottom_text + ' ' * (x - 1 - len(self.bottom_text)),
            curses.A_STANDOUT)
        try:
            self.screen.addch(y - 1, x - 1, ' ', curses.A_STANDOUT)
        except curses.error:
            pass

    def increment_letter(self, increment):
        current_letter = self.input_name[self.cursor_pos]
        ascii_alphabet_start = 97
        if current_letter.isupper():
            ascii_alphabet_start -= 32
        if current_letter == "-":
            self.input_name[self.cursor_pos] = "a"
        else:
            self.input_name[self.cursor_pos] = chr((
                (ord(current_letter) - ascii_alphabet_start + increment) %
                26) + ascii_alphabet_start)

    def change_letter_case(self):
        current_letter = self.input_name[self.cursor_pos]
        if current_letter.isupper():
            self.input_name[self.cursor_pos] = current_letter.lower()
        else:
            self.input_name[self.cursor_pos] = current_letter.upper()

    def add_channel(self):
        params = channel = {
            "name": self.channel_name,
            "password": self.user_password
        }
        create_channel(params)
        self.user_password = None
        self.running = False

    def set_channel_info(self):
        self.user_password = None
        channel_name = []
        for letter in self.input_name:
            if letter == "_":
                break
            channel_name.append(letter)
        self.channel_name = "".join(channel_name)
        if self.pass_choice:
            password_input = PasswordView(next_screen=self,
                                          global_state=self.global_state,
                                          top_text="Stwórz hasło:").show(
                                              self.screen)
        else:
            self.add_channel()

    def event_loop(self):
        char_code = self.screen.getch()

        if char_code == ord('q'):
            self.running = False

        if char_code == curses.KEY_UP:
            self.increment_letter(1)

        if char_code == curses.KEY_DOWN:
            self.increment_letter(-1)

        if char_code == curses.KEY_LEFT:
            self.cursor_pos = (self.cursor_pos - 1) % 5

        if char_code == curses.KEY_RIGHT:
            self.cursor_pos = (self.cursor_pos + 1) % 5

        if char_code == ord("p"):
            self.pass_choice = (self.pass_choice + 1) % 2

        if char_code == ord("u"):
            self.change_letter_case()

        if char_code == 10 or char_code == curses.KEY_ENTER:
            self.set_channel_info()
