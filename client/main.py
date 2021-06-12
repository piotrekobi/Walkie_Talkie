import time

from call_controler import CallController
from cli_app import CLIApp, GenericView, SelectView, ListView, CallView
from config.server import SERVER_URL, MIC_PORT, SPEAKER_PORT, USER_ID
import json

if __name__ == '__main__':
    # call_controller = CallController(
    #     url=SERVER_URL,
    #     mic_port=MIC_PORT,
    #     speaker_port=SPEAKER_PORT,
    #     user_id=USER_ID
    # )

    # call_controller.connect(10)

    # while True:
    #     pass

    with open("rest_api/channels.json", "r") as f:
        channels = json.load(f)
        available_channels = 12 * [
            f"{channel['id']}: {channel['name']}" for channel in channels
        ]

    channel_choice_view = ListView(title='Wybierz kanał',
                                   top_text="Dostępne kanały:",
                                   item_list=available_channels)
    cli_app = CLIApp(
        SelectView(title='Internetowe Walkie-Talkie',
                   top_text='Wybrany kanał:',
                   options=[
                       channel_choice_view,
                       CallView(title='Rozpocznij połączenie',
                                choice_view=channel_choice_view),
                   ]))

    cli_app.run()
