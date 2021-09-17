#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        #print ("Got a request of: %s\n" % self.data)
        
        self.separate = self.data.decode().split(' ')
        #print(separate)
        #self.request.sendall(bytearray("OK",'utf-8'))
        self.its_method = self.separate[0]
        self.its_file = self.separate[1]

        if self.its_method != "GET":
            self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))
        else:
            self.path = "./www" + self.its_file
            #return index.html 
            if "../" not in self.path and os.path.exists(self.path):
                if self.path[-1] == "/":
                    self.path += "index.html"
                    self.info_list = self.read_file(self.path)
                    self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: " + self.info_list[0] + "\r\n" + self.info_list[1], "utf-8"))
                #check whether a file
                else:
                    if os.path.isfile(self.path):
                        self.info_list = self.read_file(self.path)
                        self.request.sendall(bytearray("HTTP/1.1 200 OK\r\nContent-Type: " + self.info_list[0] + "\r\n" + self.info_list[1], "utf-8"))
                    else: # 301
                        self.request.sendall(bytearray("HTTP/1.1 301 Moved Permanently\r\n",'utf-8'))



            else:
                self.request.sendall(bytearray("HTTP/1.1 404 Not Found\r\n", "utf-8"))
    #     check_method()

    # def check_method(self):
    #     if self.its_method != "GET":
    #         self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed\r\n",'utf-8'))

    def read_file(self, path):

        file_info = []
        # check mime type
        if path.endswith(".html"):
            file_info.append("text/html")
        elif path.endswith(".css"):
            file_info.append("text/css")
        else:
            file_info.append("text/plain")

        # read file
        open_file = open(path, "r")
        contents = open_file.read()
        open_file.close()

        file_info.append(contents)

        return file_info  



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
