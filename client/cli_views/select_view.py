import curses
from cli_views.generic_view import GenericView
from cli_views.password_view import PasswordView
from rest_api_func import channel_connection_info, delete_channel


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
        self.user_password = None
        self.num_options = 2

    def set_start_params(self):
        self.invalid_password = False
        if self.user_password is not None:
            if channel_connection_info(self.global_state.current_channel["id"],
                                       self.user_password).status_code == 200:
                self.delete_current_channel()
            else:
                self.invalid_password = True

    def draw(self):
        try:
            if self.invalid_password:
                wrong_password_text = "Nieprawidłowe hasło"
                self.screen.addstr(
                    5, (self.max_x - len(wrong_password_text)) // 2,
                    wrong_password_text, curses.A_STANDOUT)
            else:
                self.screen.addstr(1, (self.max_x - len(self.title)) // 2,
                                   self.title, curses.A_STANDOUT)

                self.screen.addstr(2, 3, self.top_text, curses.A_NORMAL)

                self.screen.addstr(2, 4 + len(self.top_text),
                                   self.current_channel_id, curses.A_STANDOUT)

                pos = 4
                for i in range(self.num_options):
                    style = curses.A_NORMAL

                    if i == self.cursor_pos:
                        style = curses.A_STANDOUT

                    self.screen.addstr(pos, 3, self.options[i].title, style)
                    pos += 1

                self.screen.addstr(
                    self.max_y - 1, 0, self.bottom_text + ' ' *
                    (self.max_x - 1 - len(self.bottom_text)),
                    curses.A_STANDOUT)
                try:
                    self.screen.addch(self.max_y - 1, self.max_x - 1, ' ',
                                      curses.A_STANDOUT)
                except curses.error:
                    pass
        except curses.error:
            pass

    def set_current_channel_id(self):
        self.num_options = 2
        if self.global_state.current_channel_name is not None:
            self.current_channel_id = self.global_state.current_channel_name
            self.num_options = 4

    def delete_current_channel(self):
        delete_channel(self.global_state.current_channel["id"],
                       self.user_password)
        self.current_channel_id = "Brak"
        self.global_state.current_channel_name = None
        self.global_state.current_channel = None
        self.user_password = None

    def event_loop(self):
        char_code = self.screen.getch()

        if char_code == ord('q'):
            if self.invalid_password:
                self.user_password = None
                self.show(self.screen)
            else:
                self.running = False

        if char_code == curses.KEY_UP:
            self.cursor_pos = (self.cursor_pos - 1) % self.num_options

        if char_code == curses.KEY_DOWN:
            self.cursor_pos = (self.cursor_pos + 1) % self.num_options

        if char_code == 10 or char_code == curses.KEY_ENTER:
            if self.invalid_password:
                self.user_password = None
                self.show(self.screen)
            else:
                self.global_state.download_channels()
                if self.cursor_pos == 2 and self.global_state.current_channel is not None and self.global_state.current_channel.get(
                        "has_password"):
                    PasswordView(next_screen=self.options[self.cursor_pos],
                                 global_state=self.global_state,
                                 top_text="Podaj hasło:").show(self.screen)
                elif self.cursor_pos == 3:
                    if self.global_state.current_channel["has_password"]:
                        PasswordView(next_screen=self,
                                     global_state=self.global_state,
                                     top_text="Podaj hasło:").show(self.screen)
                    else:
                        self.delete_current_channel()
                else:
                    self.options[self.cursor_pos].show(self.screen)

        self.set_current_channel_id()