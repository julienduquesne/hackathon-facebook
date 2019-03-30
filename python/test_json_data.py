from json_parser import parse_conversation
from metrics import *

message_list = parse_conversation('data.json')
print("user_leaderboard", user_leaderboard(message_list))
print("message_leaderboard", message_leaderboard(message_list))