#!/usr/bin/env python
# coding: utf-8
# Copyright 2014 Alexander Wong, Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body
    
    def __str__(self):
        return str(self.code) + '\n\r' + self.body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        return None

    def get_code(self, data):
        return int(data.split()[1])
        
    def get_headers(self,data):
        counter = 0
        data = data.splitlines()
        for i in data:
            counter += 1
            if i == "":
                break
        return "\r\n".join(data[0:counter-1])

    def get_body(self, data):
        counter = 0
        data = data.splitlines()
        for i in data:
            counter += 1
            if i == "":
                break
        return "\r\n".join(data[counter:len(data)])

    # read everything from the socket
    def recvall(self, sock, buffersize=4096):
        response = [sock.recv(buffersize)]
        while response[-1]:
            response.append(sock.recv(buffersize))
        return ''.join(response) 

    def path_host_port(self, url):
        parsed = urlparse.urlparse(url)
        try:
            host, port = parsed.netloc.split(':')
        except ValueError:
            host, port = parsed.netloc, 80
        return [parsed, host, port]
    
    def setup_socket(self, sockvals, timeout=10):
        sock = socket.create_connection((sockvals[1], sockvals[2]), timeout)
        return sock

    def GET(self, url, args=None):
        sockvals = self.path_host_port(url)
        sock = self.setup_socket(sockvals)
        sock.sendall('GET %s HTTP/1.0\n\n' % sockvals[0].geturl())
        data = self.recvall(sock)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPRequest(code, body)        

    def POST(self, url, args=None):
        sockvals = self.path_host_port(url)
        sock = self.setup_socket(sockvals)
        
        postsock = 'POST %s HTTP/1.0\n' % sockvals[0].geturl()
        if args != None:
            postdata = urllib.urlencode(args)
            postsock += ('Content-Length: '+ 
                         str(len(postdata))+'\n\n'+
                         postdata)
        else:
            postsock += "\n"
        sock.sendall(postsock)
        data = self.recvall(sock)
        code = self.get_code(data)
        body = self.get_body(data)
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print client.command( sys.argv[2], sys.argv[1] )
        
    else:
        print client.command( sys.argv[1], command )
