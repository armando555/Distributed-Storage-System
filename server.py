import socket
import threading
import constants
from http.server import HTTPServer, BaseHTTPRequestHandler
import http.client
import cgi
import sys
import json
import urllib.parse
import threading


def splitFile(file):
    #Stores the length of the string  
    length = len(file);   
    #n determines the variable that divide the string in 'n' equal parts  
    n = 2;  
    temp = 0;  
    chars = int(length/n);  
    #Stores the array of string  
    equalStr = [];   
    #Check whether a string can be divided into n equal parts  
    if(length % n != 0):  
        print("Sorry this string cannot be divided into " + str(n) +" equal parts.")
        n=3
        chars = int(length/n);  
        print("we are going to divide into 3 equal parts")
        
    for i in range(0, length, chars):  
        #Dividing string in n equal part using substring()  
        part = file[ i : i+chars];  
        equalStr.append(part);  
    print("Equal parts of given string are");  
    for i in equalStr:  
        print("*************************************************************************************************************************");  
        print(i);  




# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = constants.IP_SERVER
files = {}
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
        remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print (f'Data received from: {client_address[0]}:{client_address[1]}')
        print(command)
        
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
            #print("the request is ", requestHttp)
            conn.request("GET", requestHttp)
            firstResponse = conn.getresponse()
            firstResponse = firstResponse.read()
            #conversion = str(firstResponse)
            #splitFile(conversion.decode())
            #print("message from client 1 ",firstResponse)
            client_connection.sendall(firstResponse)
        elif (command == constants.SAVE):
            response = remote_command[1] 
            files[response] = client_address[0]
            print(files)
            response = "200 OK\n"
            client_connection.sendall(response.encode(constants.ENCONDING_FORMAT))
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






