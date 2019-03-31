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
    elif key == 'sent messages':
        user_dict = {}
        for m in message_list:
            user = m.author
            if user in user_dict:
                user_dict[user] += 1
            else:
                user_dict[user] = 1
        user_react_list = [(k, v) for k, v in user_dict.items()]
        user_react_list.sort(key=lambda t: t[1], reverse=True)
        return user_react_list
    else:
        pass


def filter_image(message_list):
    res = []
    for m in message_list:
        attachments = m.attachments
        if attachments != []:
            res.append(m)
    return res

def get_words_for_cloud(message_list):
    msgs = [m.body for m in message_list]
    counts_list = [count_words(msg) for msg in msgs]


def count_words(msg_txt):
    words = msg_txt.split()
    good_words = [correct_word(word) for word in words]
    counts = {}
    for word in good_words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def correct_word(word):
    punctuation = ['.', ',', '!', '?', '(', ')', ':', ';']
    if word[0] in punctuation:
        word.pop(0)
    if word[-1] in punctuation:
        word.pop()
    return word

def message_leaderboard(message_list, flag='all'):
    if flag=='all':
        l = sorted(message_list, key=lambda m: len(m.reactions), reverse=True)
        res = [{"author": m.author, "reactions":m.reactions, "body": m.body, "timestamp": m.timestamp} for m in l]
        return res
    elif flag=='images':
        l = sorted(filter_image(message_list), key=lambda m: len(m.reactions), reverse=True)
        res = [{"author": m.author, "reactions":m.reactions, "body": m.body, "timestamp": m.timestamp} for m in l]
        return res


def user_index(message_list):
    user_dict, cpt = {}, 0
    for m in message_list():message_list
        user = m.author
        if user not in user_dict:
            user_dict[user] = cpt
            cpt += 1
    return user_dict, cpt


def sym_adjacency_dict(message_list):
    user_dict = {}
    for m in message_list:
        user = m.author
        if user not in user_dict:
            user_dict[user] = {}
        user_reactions = user_dict[user]
        for r in m.reactions:
            reaction_giver = r["userID"]
            # reaction_giver reacts to user
            if reaction_giver in user_reactions:
                user_reactions[reaction_giver] += 1
            else:
                user_reactions[reaction_giver] = 1
            # user receives reaction from reaction_giver
            if reaction_giver in user_dict:
                if user in user_dict[reaction_giver]:
                    user_dict[reaction_giver][user] += 1
                else:
                    user_dict[reaction_giver][user] = 1
            else:
                user_dict[reaction_giver] = {user: 1}
    return user_dict


def filter_sym_dict(d, nb=3):
    user_best_friends = {}
    for user in d:
        l = [(k, v) for k, v in d[user].items()]
        l.sort(key=lambda t: t[1], reverse=True)
        user_best_friends[user] = l[:min(nb, len(l))]
    return user_best_friends


