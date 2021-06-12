import requests

URL = "http://127.0.0.1:5000/channels"


def get_channels():
    return requests.get(f"{URL}")


def channel_info(channel_id):
    return requests.get(f"{URL}/{channel_id}")


def channel_connection_info(channel_id, password):
    return requests.get(f"{URL}/{channel_id}/{password}")


def delete_channel(channel_id, password=None):
    if password:
        return requests.delete(f"{URL}/{channel_id}/{password}")
    return requests.delete(f"{URL}/{channel_id}")


def create_channel(params):
    return requests.post(f"{URL}", json=params)