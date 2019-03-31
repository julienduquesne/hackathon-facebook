from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
import os
import requests
from json_parser import *
from metrics import *
import json
import numpy as np

url_for_node = "http://node:3000/output_python"

wanted_features = ['received reactions', 'given reactions', 'sent messages']
messages_flags = ['all', 'images']
store_path = '/raw_conversation'

# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):
    def _set_response(self,output):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()
        self.wfile.write(output.encode('utf-8'))

    def do_GET(self):
        return

    def do_POST(self):
        print('Message received')
        if self.path == store_path:
            content_len = int(self.headers['Content-Length'])
            input_conv = self.rfile.read(content_len).decode('utf-8')
            print(type(input_conv))
            # call python computations
            output_python = output_metrics(input_conv)
            print(output_python)
            self._set_response(output_python)


def output_metrics(input_conv):
    message_list = parse_conversation(input_conv)
    output = {}
    for feature in wanted_features:
        output[feature] = user_leaderboard(message_list, key=feature)

    for flag in messages_flags:
        output[flag] = message_leaderboard(message_list, flag=flag)

    nodes = [{'id': user, 'value': value, 'label': 'fill name', 'scaling.label': True}
             for (user, value) in output['sent messages']]
    nodes = scale_node_values(nodes)
    filtered_adjacency_dic = filter_sym_dict(sym_adjacency_dict(message_list))
    edges = []
    for user, friends in filtered_adjacency_dic.items():
        for i in range(len(friends)):
            if {'from': friends[i][0], 'to': user, 'value': friends[i][1]} not in edges:
                edges.append({'from': user, 'to': friends[i][0],
                              'value': friends[i][1]})
    output["graph_data"] = {'nodes': nodes, 'edges': edges}
    return json.dumps(output)


def scale_node_values(list_nodes, min=5, max=150):
    nodes = list_nodes
    values = np.array([node['value'] for node in nodes])
    min_v = min(values)
    max_v = max(values)
    scale = max_v - min_v
    scaled_values = values - min_v
    scaled_values = scaled_values / scale
    scaled_values = max * scaled_values + min
    for i, node in enumerate(nodes):
        node['value'] = scaled_values[i]
    return list_nodes

def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('0.0.0.0', 8081)
    httpd = HTTPServer(server_address, TestHTTPServer_RequestHandler)
    print('running server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


run()
