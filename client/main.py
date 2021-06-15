from cli_app import CLIApp, GlobalState
from cli_views.add_view import AddView
from cli_views.call_view import CallView
from cli_views.generic_view import GenericView
from cli_views.list_view import ListView
from cli_views.select_view import SelectView

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
                       AddView(title="Dodaj kanał", global_state=global_state),
                       CallView(title='Rozpocznij połączenie',
                                global_state=global_state),
                       GenericView(title="Usuń wybrany kanał",
                                   global_state=global_state)
                   ]))

    cli_app.run()
