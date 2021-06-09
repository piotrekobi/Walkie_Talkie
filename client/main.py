from call_controler import CallController
from cli_app import CLIApp, GenericView, SelectView, ListView
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
        available_channels = 15 * [
            f"{channel['id']}: {channel['name']}" for channel in channels
        ]

    cli_app = CLIApp(
        SelectView(title='Internetowe Walkie-Talkie',
                   options=[
                       ListView(title='Zobacz Dostępne kanały',
                                top_text="Dostępne kanały:",
                                item_list=available_channels),
                       GenericView(title='Rozpocznij połączenie'),
                   ]))

    cli_app.run()
