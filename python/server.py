from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
import os
import requests
from json_parser import *
from metrics import *
import json

url_for_node = "http://localhost:3000/output_python"

wanted_features = ['received reactions', 'given reactions', 'sent messages']
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

    nodes = [{'id': user, 'value': value, 'label': 'fill name'}
             for (user, value) in output['sent messages']]
    filtered_adjacency_dic = filter_sym_dict(sym_adjacency_dict(message_list))
    edges = []
    for user, friends in filtered_adjacency_dic.items():
        for i in range(len(friends)):
            if {'from': friends[i][0], 'to': user, 'value': friends[i][1]} not in edges:
                edges.append({'from': user, 'to': friends[i][0],
                              'value': friends[i][1]})
    output["graph_data"] = {'nodes': nodes, 'edges': edges}
    return json.dumps(output)


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('', 8081)
    httpd = HTTPServer(server_address, TestHTTPServer_RequestHandler)
    print('running server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


run()
