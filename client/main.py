import time
from call_controler import CallController
from cli_app import CLIApp, GlobalState
from cli_views import GenericView, SelectView, ListView, CallView, PasswordView

if __name__ == '__main__':
    global_state = GlobalState()
    cli_app = CLIApp(
        SelectView(title='Internetowe Walkie-Talkie',
                   top_text='Wybrany kanał:',
                   global_state=global_state,
                   options=[
                       ListView(title='Wybierz kanał',
                                top_text="Dostępne kanały:",
                                global_state=global_state),
                       CallView(title='Rozpocznij połączenie',
                                global_state=global_state),
                       PasswordView(title="test",
                                    global_state=global_state,
                                    top_text="Hasło:")
                   ]))

    cli_app.run()
