import numpy as np
import json


class User:

    def __init__(self, name, user_id):
        self.name = name
        self.user_id =  user_id
        self.msg_sent = []
        self.react_received = []
        self.react_given = []

    def get_msg_sent(self):
        pass

    def get_number_of_msg(self, start, stop):
        pass

    def get_all_reacts(self):
        pass

    def get_react_received(self, start, stop):
        pass

    def get_react_given(self, start, stop):
        pass
