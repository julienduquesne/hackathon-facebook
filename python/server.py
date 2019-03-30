from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
import os
import requests
from json_parser import *
from metrics import *

url_for_node = "http://localhost:3000/output_python"

wanted_features = ['received reactions', 'given reactions', 'sent messages']
store_path = '/raw_conversation'

# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):

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
            r = requests.post(url_for_node, data={'data':output_python})

            self.send_response(200)


def output_metrics(input_conv):
    message_list = parse_conversation(input_conv)
    output = {}
    for feature in wanted_features:
        output[feature] = user_leaderboard(message_list, key=feature)
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
