from flask import Flask
from flask_restful import Resource, Api
import json

app = Flask(__name__)
api = Api(app)

with open("channels.json", "r") as f:
    channels = json.load(f)


class Channels(Resource):
    def get(self):
        channel_list = [{"id": c["id"], "name": c["name"]} for c in channels]
        return channel_list


class ChannelId(Resource):
    def get(self, channel_id):
        try:
            return f"channel_id - {channels[channel_id - 1].get('name')}"
        except IndexError:
            return "Invalid channel ID"


class ChannelIdPass(Resource):
    def get(self, channel_id, password):
        try:
            channel = channels[channel_id - 1]
            if channel["password"] == password:
                return channel
            else:
                return "Wrong password"

        except IndexError:
            return "Invalid channel ID"


api.add_resource(Channels, '/channels')
api.add_resource(ChannelId, '/channels/<int:channel_id>')
api.add_resource(ChannelIdPass, '/channels/<int:channel_id>/<string:password>')

if __name__ == "__main__":
    app.run(debug=True)
