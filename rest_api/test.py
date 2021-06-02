from api_func import *

channel = {"name": "fff", "password": "555"}
print(get_channels().text)
print(channel_info(1).text)
print(channel_connection_info(1, "000").text)
print(delete_channel(4).text)
print(delete_channel(1, "000").text)
print(create_channel(channel).text)