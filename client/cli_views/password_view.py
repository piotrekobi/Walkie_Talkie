import curses
import curses.textpad
from cli_views.generic_view import GenericView


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
        try:
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
                y - 1, 0,
                self.bottom_text + ' ' * (x - 1 - len(self.bottom_text)),
                curses.A_STANDOUT)
            try:
                self.screen.addch(y - 1, x - 1, ' ', curses.A_STANDOUT)
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