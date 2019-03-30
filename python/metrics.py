from message import Message
import json
from json_parser import parse_conversation


def message_by_users(message_list):
    user_dict = {}
    for m in message_list:
        user = m.author
        if user in user_dict:
            user_dict[user].append(m)
        else:
            user_dict[user] = [m]
    return user_dict


def user_leaderboard(message_list, key='received reactions'):
    user_react_list = []
    if key == 'received reactions':
        for user, messages in message_by_users(message_list).items():
            nb_react = 0
            for m in messages:
                nb_react += len(m.reactions)
            user_react_list.append((user, nb_react))
        user_react_list.sort(key=lambda t: t[1], reverse=True)
        return user_react_list
    elif key == 'given reactions':
        user_dict = {}
        for m in message_list:
            for r in m.reactions:
                user = r["userID"]
                if user in user_dict:
                    user_dict[user] += 1
                else:
                    user_dict[user] = 1
        user_react_list = [(k, v) for k, v in user_dict.items()]
        user_react_list.sort(key=lambda t: t[1], reverse=True)
        return user_react_list
    else:
        pass





def message_leaderboard(message_list):
    return sorted(message_list, key=lambda m: len(m.reactions), reverse=True)
