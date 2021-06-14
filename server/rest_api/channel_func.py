import json
from flask import error

def load_channels(filename):
    with open(filename, "r") as f:
        return json.load(f)


def save_channels(filename, channels):
    with open(filename, "w") as f:
        json.dump(channels, f)


def find_channel(channel_id, channels):
    for i, channel in enumerate(channels):
        if channel["id"] == channel_id:
            return i, channel
    return None, None


def delete_channel(channel_id, channels, password=None):
    index, channel = find_channel(channel_id, channels)
    if channel and channel["password"] == password:
        channels.pop(index)
        save_channels("../data/channels.json", channels)
        return "Channel deleted"
    return "Invalid channel ID or password"


def create_channel(info, channels):
    try:
        channels.append({
            "id": channels[len(channels) - 1]["id"] + 1,
            "name": info["name"],
            "password": info["password"]
        })
        save_channels("../data/channels.json", channels)
        return "Channel created"
    except KeyError:
        return "Invalid channel info"


def channel_info(channel_id, channels):
    _, channel = find_channel(channel_id, channels)
    if channel:
        return {"id": channel["id"], "name": channel["name"]}
    return "Invalid channel ID"


def detailed_channel_info(channel_id, channels, password):
    _, channel = find_channel(channel_id, channels)
    if channel and (channel["password"] == password or channel["password"] is None):
        return channel, 200
    return "Invalid channel ID or password", 401