from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
import sys
import json
import socket
import urllib.parse
import threading
import constants
import pickle
import os.path
import cv2
import random




client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)



files = []



class helloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content_type', 'application/octet-stream')
        self.end_headers()
        file = self.path[1:]
        d = open(self.path[1:],"rb")
        file = d.read()
        self.wfile.write(file)
    def do_POST(self):
        print("ESTOY HACIENDO POST JEJE")
        content_len = int(self.headers.get('content-length'))
        post_body = self.rfile.read(content_len)
        print(type(post_body))
        print(post_body)
        print(self.path[1:])
        name = self.headers.get('fileName')
        data = post_body
        file = open(name,"wb")
        file.write(data)
        file.close()
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(bytes("okey","utf-8"))





def main():
    PORT = 53000
    server = HTTPServer(('', PORT), helloHandler)
    print(f'server running on port {PORT}')
    threads = []
    tServer = threading.Thread(target=server.serve_forever)
    threads.append(tServer)
    tServer.start()



    print('***********************************')
    print('Client is running...')
    client_socket.connect((constants.IP_SERVER,constants.PORT))
    local_tuple = client_socket.getsockname()
    print('Connected to the server from:', local_tuple)
    print('Enter \"quit\" to exit')
    print('What do you want to do?\nDownload\nSave')
    command_to_send = input()



    while command_to_send != constants.QUIT:
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()
        elif (command_to_send == constants.DOWNLOAD):
            data_to_send = input('Input data to download: ')
            command_and_data_to_send = command_to_send + ' ' + data_to_send
            command_and_data_to_send = pickle.dumps(command_and_data_to_send)
            client_socket.send(command_and_data_to_send)
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print("papi la recibi como es")
            d = pickle.loads(data_received)
            #file = open(data_to_send,"w")
            #file.write(d)
            #file.close()
            print(d)
            print(type(d))
            cv2.imwrite(data_to_send,d)
            print("200 OK")
            command_to_send = input()
        elif (command_to_send == constants.SAVE):
            data_to_send = input('Input data to save: ')
            name = data_to_send
            files.append(data_to_send)
            d = cv2.imread(data_to_send)
            data = pickle.dumps(d)
            data_to_send = {}
            data_to_send["command"] = command_to_send
            data_to_send["name"] = name
            data_to_send["data"] = data
            data_to_send = pickle.dumps(data_to_send)
            client_socket.send(data_to_send)
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()
        else:
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
            print(data_received.decode(constants.ENCONDING_FORMAT))
            command_to_send = input()



    client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
    data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
    print(data_received.decode(constants.ENCONDING_FORMAT))
    print('Closing connection...BYE BYE...')
    client_socket.close()




if __name__ == "__main__":
    main()