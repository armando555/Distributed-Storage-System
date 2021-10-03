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
        if os.path.isfile(file):
            d = cv2.imread(file)
            msg = pickle.dumps(d)
            self.wfile.write(msg)
        else:
            msg = "No, sorry I dont have it " + file
            self.wfile.write(pickle.dumps(msg))
    
        


def main():
    PORT = 53000
    server = HTTPServer(('localhost', PORT), helloHandler)
    print(f'server running on port {PORT}')
    threads = []
    tServer = threading.Thread(target=server.serve_forever)
    threads.append(tServer)
    tServer.start()

    print('***********************************')
    print('Client is running...')
    client_socket.connect(("127.0.0.1",constants.PORT))
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
            d = pickle.loads(data_received)
            cv2.imwrite(data_to_send,d)
            cv2.imshow('Imagen',d)
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
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
