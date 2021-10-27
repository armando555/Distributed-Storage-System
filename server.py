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
    originalCode = bytesFile
    print(len(bytesFile))
    n_iteracions = len(bytesFile) / 1024
    if isinstance(n_iteracions, float):
        n_iteracions = int(n_iteracions) + 1
    print(n_iteracions)
    chunks = []
    min_limit = 0
    max_limit = 1024
    names = []
    counter = 0
    name_cons = name
    # ACA ESCRIBO LOS BYTES EN EL ARCHIVO
    for i in range(n_iteracions):
        print(name)
        if counter == 1:
            name = name_cons + '1'
        else:
            name = name_cons + str(counter)
        names.append(name)
        file = open(name, 'wb')
        file.write(bytesFile[min_limit:max_limit])
        chunks.append(bytesFile[min_limit:max_limit])
        file.close()
        min_limit = max_limit
        max_limit += 1024
        counter += 1
        files[nameR] = names
    return chunks


# Defining a socket object...
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = constants.IP_SERVER

#Client1 = [logo.jpg0,...]
clientAdresses = {}


def main():

    print("***********************************")


    print("Server is running...")
    print("Dir IP:", server_address)
    print("Port:", constants.PORT)
    server_execution()

# Handler for manage incomming clients conections...


def handler_client_connection(client_connection, client_address):


    clientAdresses[client_address[0]] = []
    clientParts = {}
    print(
        f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
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
        print(f'Data received from: {client_address[0]}:{client_address[1]}')
        if (command == constants.QUIT):
            response = '200 BYE\n'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
            is_connected = False
        elif (command == constants.DOWNLOAD):
            bytesTotal = b''
            #conn = http.client.HTTPConnection("127.0.0.1",53000)
            #requestHttp = "/JulianEllindo"
            #conn.request("GET", requestHttp)
            #firstResponse = conn.getresponse()
            #firstResponse = firstResponse.read()
            #bytesTotal = bytesTotal + firstResponse
            #conn = http.client.HTTPConnection("127.0.0.1",54000)
            #requestHttp = "/Armando"
            #conn.request("GET", requestHttp)
            #firstResponse = conn.getresponse()
            #firstResponse = firstResponse.read()
            #bytesTotal = bytesTotal + firstResponse
            print(clientAdresses)
            if(files[remote_command[1]] != ''):
                for client in clientAdresses.keys():
                    chunk_request = ''
                    for chunk in clientAdresses[client]:
                        print(remote_command[1])
                        print(chunk)
                        print(remote_command[1] in chunk)
                        print(remote_command[1] != chunk)
                        if remote_command[1] in chunk and remote_command[1] != chunk:
                            chunk_request = chunk

                    if chunk_request != '':
                        print(chunk_request)
                        print("papi va a preguntar por este", chunk_request)
                        conn = http.client.HTTPConnection(client, 53000)
                        requestHttp = "/" + chunk_request
                        print("the request is ", requestHttp)
                        conn.request("GET", requestHttp)
                        firstResponse = conn.getresponse()
                        firstResponse = firstResponse.read()
                        bytesTotal = bytesTotal + firstResponse
                        print("message from client "+str(client)+str(firstResponse))
                        print("finished")
                        print("lo que diga armando")
                        print(bytesTotal)
                client_connection.sendall(bytesTotal)

        elif (command == constants.SAVE):
            data = remote_command[1]
            # cv2.imshow('Imagen',pickle.loads(data))
            # cv2.waitKey(5000)
            # cv2.destroyAllWindows()
            #files[remote_command[2]] = client_address[0]
            chunks = splitFile(data, remote_command[2])
            count = 0
            for client in clientAdresses.keys():
                conn = http.client.HTTPConnection(client, 53000)
                headers = {'Content-type': 'application/octet-stream',
                           'fileName': remote_command[2]+str(count)}
                file = open(remote_command[2]+str(count), "rb")
                print('conectado')
                data = file.read()
                conn.request('POST', '/post', data, headers)
                clientAdresses[client].append(remote_command[2]+str(count))
                count += 1

#conn = http.client.HTTPConnection("127.0.0.1",53000)
#file = open("logo.jpg0","rb")
#data = file.read()
#headers = {'Content-type': 'application/octet-stream','fileName':'Julian'}
# clientAdresses[client_address[0]].append("Julian")
#clientParts ["Julian"] = client_address[0]
#conn.request('POST', '/post/', data, headers)
#count += 1
#conn = http.client.HTTPConnection("127.0.0.1",54000)
#file = open("logo.jpg01","rb")
#data = file.read()
#headers = {'Content-type': 'application/octet-stream','fileName':'Armando'}
# clientAdresses[client_address[0]].append("Armando")
#clientParts ["Armando"] = client_address[0]
#conn.request('POST', '/post/', data, headers)
#count += 1
                print(files)
                response = "200 OK\n"
                client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        else:
            response = '400 BCMD\n\rCommand-Description: Bad command\n\r'
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
        print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
        client_connection.close()

# Function to start server process...


def server_execution():


    tuple_connection = (socket.gethostname(), constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(
        target=handler_client_connection, args=(client_connection, client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()

if __name__ == "__main__":
    main()
