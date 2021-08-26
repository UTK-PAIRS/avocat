'''
    Local.py:
        Creates the local site that will hold the
        suggestions from avocat.

    Guide intially used: https://pythonbasics.org/webserver/
''' 

from http.server import BaseHTTPRequestHandler, HTTPServer
import time




#   Server Class    #
class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        self.wfile.write("FOOBAR".encode())

def run():
    
    #   Random port numeer, could change    #
    hostName = "localhost"
    portNumber = 8000
    server = HTTPServer(('localhost', portNumber), Server)
    print("Server running on: %s" % portNumber)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()

    


run()
