import time
from call_controler import CallController
from cli_app import CLIApp, GlobalState
from cli_views import GenericView, SelectView, ListView, CallView
import rest_api_func

if __name__ == '__main__':

    # call_controller.connect(10)

    # while True:
    #     pass

    global_state = GlobalState()
    channels = rest_api_func.get_channels().json()
    available_channels = [
        f"{channel['id']}: {channel['name']}" for channel in channels
    ]

    cli_app = CLIApp(
        SelectView(title='Internetowe Walkie-Talkie',
                   top_text='Wybrany kanał:',
                   global_state=global_state,
                   options=[
                       ListView(title='Wybierz kanał',
                                top_text="Dostępne kanały:",
                                item_list=available_channels,
                                global_state=global_state),
                       CallView(title='Rozpocznij połączenie',
                                global_state=global_state),
                   ]))

    cli_app.run()
