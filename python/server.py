from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
import os
import requests
import urlparse
from json_parser import *
from metrics import *

PATH_upload_json = "http://localhost:8081/"
url_for_node = "http://localhost:8000/output_python"

wanted_features = ['received reactions', 'given reactions', 'sent messages']
# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    store_path = os.path.join(curdir, 'raw_conversation')

    def do_GET(self):
        return

    def do_POST(self):
        if self.path == PATH_upload_json:
            content_len = int(self.headers.getheader('content-length', 0))
            input_conv = self.rfile.read(content_len).decoder('utf-8')

            # call python computations
            output_python = output_metrics(input_conv)

            r = requests.post(url_for_node, data=output_python)

            self.send_response(200)


def output_metrics(input_conv):
    message_list = parse_conversation(input_conv)
    output = {}
    for feature in wanted_features:
        output[feature] = user_leaderboard(message_list, key=feature)
    return output


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('127.0.0.1', 8081)
    httpd = HTTPServer(server_address, TestHTTPServer_RequestHandler)
    print('running server...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


run()
