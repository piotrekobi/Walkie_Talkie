from flask import Flask, request
from flask_restful import Resource, Api

from channel_func import find_channel, delete_channel, channel_info, \
     detailed_channel_info, create_channel, load_channels

app = Flask(__name__)
api = Api(app)
channels = load_channels("channels.json")


class Channels(Resource):
    def get(self):
        return [{"id": c["id"], "name": c["name"]} for c in channels]

    def post(self):
        return create_channel(request.get_json(), channels)


class ChannelId(Resource):
    def get(self, channel_id):
        return channel_info(channel_id, channels)

    def delete(self, channel_id):
        return delete_channel(channel_id, channels)


class ChannelIdPass(Resource):
    def get(self, channel_id, password):
        return detailed_channel_info(channel_id, channels, password)

    def delete(self, channel_id, password):
        return delete_channel(channel_id, channels, password)


api.add_resource(Channels, '/channels')
api.add_resource(ChannelId, '/channels/<int:channel_id>')
api.add_resource(ChannelIdPass, '/channels/<int:channel_id>/<string:password>')

if __name__ == "__main__":
    app.run(debug=True)
