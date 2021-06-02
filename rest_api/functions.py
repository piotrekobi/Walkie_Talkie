import requests


def _url(path):
    return "https://test-project-domain.com" + path


def get_channels():
    return requests.get(_url("channels"))


def channel_info(channel_id):
    try:
        return requests.get(_url(f"channels/{channel_id}"))
    except ConnectionError:
        print("Invalid channel ID")


def channel_connection_info(channel_id, password):
    return requests.get(_url(f"/channels/{channel_id}/{password}"))


def delete_channel(channel_id):
    r = requests.delete(_url(f"channels/{channel_id}"))
    return r.status_code


def create_channel(params):
    r = requests.post(_url("/channels"), json=params)
    return r.status_codes


r = requests.get("http://127.0.0.1:5000/")
print(r.json())