#!/usr/bin/env python
import os
import json
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
import SimpleHTTPServer
import time
#import RPi.GPIO as GPIO

# Imports our libraries.
import audio
import game


class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/getRound":
            response = game.getRound()
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            print json.dumps(response)
            self.wfile.write(json.dumps(response))

        elif self.path == "/getScore":
            self.send_response(200)
            self.send_header('Content-type','application/json')
            self.end_headers()
            self.wfile.write(json.dumps(game.getScore()))
            
        else:
            SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def translate_path(self, path):
        print "path: " + path

        if path == "/song":
            print "play a song"

        elif path == "/reset":
            game.init()
        elif path == "/resetScore":
            print "hi"
        elif path == ("/join/red"):
            game.joinTeam("red")
        elif path == ("/join/blue"):
            game.joinTeam("blue")
        elif path == ("/correct/red"):
            game.correct("red")
        elif path == ("/correct/blue"):
            game.correct("blue")
        else:
            print "Unkown command: " + path

        return path[1:]



# This code will only run if this file is run as the main python file.
if __name__ == '__main__':
    print "Setup hardware interrupts."
    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(7,GPIO.OUT)
    game.init()
    print "Start server"
    httpd = HTTPServer(('0.0.0.0', 8000), MyHandler)
    httpd.serve_forever()
    print "Code here and below won't run."
