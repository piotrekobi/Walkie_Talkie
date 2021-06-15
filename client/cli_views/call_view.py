import curses
import time
from cli_views.generic_view import GenericView
from rest_api_func import channel_connection_info
from call_controler import CallController
from config.server import SERVER_URL, MIC_PORT, SPEAKER_PORT, USER_ID


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
        try:
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
                self.screen.addstr(1, (x - len(self.top_text)) // 2,
                                   self.top_text, curses.A_STANDOUT)

                call_time = round(time.time() - self.start_time)
                minutes, seconds = divmod(call_time, 60)
                time_text = f"Czas rozmowy: {minutes:02d}:{seconds:02d}"
                self.screen.addstr(3, (x - len(time_text)) // 2, time_text,
                                   curses.A_NORMAL)

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