from flask import Flask, request
from flask_restful import Api, Resource

from rest_api.channel_func import delete_channel, channel_info, detailed_channel_info, create_channel, load_channels

channels = load_channels("./data/channels.json")


# Klasa obsługuje metody get i post o adresach "/channels"
class Channels(Resource):
    def get(self):
        return [{
            "id": c["id"],
            "name": c["name"],
            "has_password": c["password"] is not None
        } for c in channels]

    def post(self):
        return create_channel(request.get_json(), channels)


# Klasa obsługuje metody get i delete o adresach "/channels/channel_id"
class ChannelId(Resource):
    def get(self, channel_id):
        return channel_info(channel_id, channels)

    def delete(self, channel_id):
        return delete_channel(channel_id, channels)


# Klasa obsługuje metody get i delete o adresach "/channels/channel_id/password"
class ChannelIdPass(Resource):
    def get(self, channel_id, password):
        return detailed_channel_info(channel_id, channels, password)

    def delete(self, channel_id, password):
        return delete_channel(channel_id, channels, password)


class FlaskRunner:
    def __init__(self):
        self.name = 'FlaskRunner'

        self.app = Flask(__name__)
        self.api = Api(self.app)

        self.api.add_resource(Channels, '/channels')
        self.api.add_resource(ChannelId, '/channels/<int:channel_id>')
        self.api.add_resource(ChannelIdPass,
                              '/channels/<int:channel_id>/<string:password>')

    def run(self):
        print(self.name, 'starting...')
        self.app.run(host='0.0.0.0', )
