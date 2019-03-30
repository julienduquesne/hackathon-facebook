import json
from message import Message


def parse_conversation(conv):
    conversation = json.loads(conv)
    messages_list = []
    for json_message in conversation:
        if json_message["type"] == 'message':
            messages_list.append(parse_message(json_message))
    return messages_list


def parse_message(m):
    message = Message(author=m["senderID"], body=m["body"],
                      timestamp=m["timestamp"], reactions=m["messageReactions"])
    return message








