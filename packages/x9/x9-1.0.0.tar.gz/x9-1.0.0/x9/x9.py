# x9.py

from gui import GUIPlus as gui
from improved_math import ImprovedMath as maths
import logging
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

logging.getLogger('wsgiref').setLevel(logging.INFO)

class SilentWSGIServer(WSGIServer):
    def log_request(self, format, *args):
        # Suppress the log entries from the WSGI server
        pass

class web:
    def __init__(self):
        self.routes = {}
        logging.getLogger('wsgiref').setLevel(logging.WARNING)

    def new(self, view_func, rule, **options):
        self.routes[rule] = view_func

    def run(self, host='localhost', port=8080):
        from wsgiref.simple_server import make_server

        print(f"Serving on http://{host}:{port}")
        server = make_server(host, port, self.dispatch, server_class=SilentWSGIServer)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

    def dispatch(self, environ, start_response):
        path = environ['PATH_INFO']
        view_func = self.routes.get(path)

        if view_func is not None:
            response_body = view_func()
            response_body = self.encode_response(response_body)  # Automatically encode the response to bytes
            status_code = '200 OK'
        else:
            response_body = b"Not Found"
            status_code = '404 Not Found'

        start_response(status_code, [('Content-Type', 'text/html')])

        # Custom log message without the server's default messages
        print(f"X9 {environ['REQUEST_METHOD']} {path} {status_code.split()[0]}")

        return [response_body]

    def encode_response(self, response_data):
        if isinstance(response_data, str):
            response_data = response_data.encode('utf-8')
        return response_data

    def html(self, file_name):
        with open(file_name, 'rb') as f:  # Open the file in binary mode
            return f.read()
