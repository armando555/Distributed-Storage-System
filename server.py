import socket
import threading
import constants
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
import cgi
import sys
import json
import pickle
import cv2
import urllib.parse
import threading

files = {}
        


def splitFile(bytesFile, name):
    nameR = name
    print(len(bytesFile))
    n_iteracions = len(bytesFile) / 1024
    if isinstance(n_iteracions,float):
        n_iteracions = int(n_iteracions) + 1
    print(n_iteracions)
    chunks = []
    min_limit = 0
    max_limit = 1024
    names = []
    #ACA ESCRIBO LOS BYTES EN EL ARCHIVO
    for i in range (n_iteracions):
        name = name + str(i)
        names.append(name)
        file = open (name,'wb')
        file.write(bytesFile[min_limit:max_limit])
        chunks.append(bytesFile[min_limit:max_limit])
        file.close()
        min_limit = max_limit
        max_limit += 1024
    files[nameR] = names




# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = constants.IP_SERVER

clientAdresses = []
#CL1: IP, PUERTO SOCKET, PUERTO HTTP
def main():

    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    
# Handler for manage incomming clients conections...

def handler_client_connection(client_connection,client_address):
    clientAdresses.append(client_address)
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)
        data_recevived = pickle.loads(data_recevived)
        remote_command = []
        if type(data_recevived) is dict:
            remote_command.append(data_recevived["command"])
            remote_command.append(data_recevived["data"]) 
            remote_command.append(data_recevived["name"])
            print(remote_command[0])
            command = remote_command[0]
        else:
            remote_command = data_recevived.split()
            command = remote_command[0]
            print(command)
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        
        
        if (command == constants.HELO):
            response = '100 OK\n'
            print(clientAdresses)
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        elif (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            is_connected = False
        elif (command == constants.DOWNLOAD):
            print(files[remote_command[1]] != '')            
            conn = http.client.HTTPConnection(files[remote_command[1]],53000)
            requestHttp = "/" + remote_command[1]
            print("the request is ", requestHttp)
            conn.request("GET", requestHttp)
            firstResponse = conn.getresponse()
            firstResponse = firstResponse.read()
            print("message from client 1 ",firstResponse)
            client_connection.sendall(firstResponse)
        elif (command == constants.SAVE):
            data = remote_command[1]
            cv2.imshow('Imagen',pickle.loads(data))
            cv2.waitKey(5000)
            cv2.destroyAllWindows()
            #files[remote_command[2]] = client_address[0]
            splitFile(data, remote_command[2])
            print(files)
            response = "200 OK\n"
            #client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            while True:
                a = 1
        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()

#Function to start server process...
def server_execution():
    tuple_connection = (server_address,constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()






