import curses
from cli_views.generic_view import GenericView
from cli_views.password_view import PasswordView
from rest_api_func import create_channel

# Klasa tworzy widok pozwalający na dodawanie nowych kanałów
class AddView(GenericView):
    def __init__(self, title, global_state, bottom_text=None):
        super().__init__(title, global_state, bottom_text=bottom_text)
        self.top_text = "Dodawanie kanału"
        self.password_options = ["Nie", "Tak"]
        self.user_password = None
        self.bottom_text = '  u - zmiana wielkości litery  ENTER - utworzenie kanału'
        self.bottom_text_2 = '  q - powró† do menu           p  - przełączenie ustawienia hasła'

    def set_start_params(self):
        self.input_name = ["_", "_", "_", "_", "_"]
        self.cursor_pos = 0
        self.pass_choice = 0

        if self.user_password is not None:
            self.add_channel()

    def draw(self):
        try:
            self.screen.addstr(1, (self.max_x - len(self.top_text)) // 2,
                               self.top_text, curses.A_STANDOUT)
            text_pos_x = self.max_x // 6
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
                self.max_y - 2, 0, self.bottom_text_2 + ' ' *
                (self.max_x - 1 - len(self.bottom_text_2)), curses.A_STANDOUT)

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
        if self.channel_name == "":
            self.channel_name = "def"
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