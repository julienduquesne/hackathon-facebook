from message import Message
import json
from parser import parse_conversation


def message_by_users(message_list):
    user_dict = {}
    for m in message_list:
        user = m.author
        if user in user_dict:
            user_dict[user].append(m)
        else:
            user_dict[user] = [m]
    return user_dict


def leaderboard(message_list):
    user_react_list = []
    for user, messages in message_by_users(message_list).items():
        nb_react = 0
        for m in messages:
            nb_react += len(m.reactions)
        user_react_list.append((user, nb_react))
    user_react_list.sort(key=lambda t: t[1], reverse=True)
    return user_react_list