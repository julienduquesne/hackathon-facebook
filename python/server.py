from http.server import BaseHTTPRequestHandler, HTTPServer
from os import curdir
import os
import requests

PATH_upload_json = "http://localhost:8081/"
url_for_node = "http://localhost:8000/output_python"


# HTTPRequestHandler class
class TestHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    store_path = os.path.join(curdir, 'raw_conversation')

    def do_GET(self):
        return

    def do_POST(self):
        if self.path == PATH_upload_json:
            content_len = int(self.headers.getheader('content-length', 0))
            post_body = self.rfile.read(content_len)

            # call python computations
            output_python = None

            r = requests.post(url_for_node, data=output_python)

            self.send_response(200)




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
