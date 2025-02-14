"""
CP372 Programming Assignment
Ryan Chisholm - Michael Wu
February 10th 2025

Server side source code
"""
import socket
import threading
import datetime
import os

HOST = "127.0.0.1"
PORT = 12345
MAX_CLIENTS = 3
clients = {} #dictionary to store client info and act as cache

def handle_client(client_socket, client_address, client_id):
    """
    Function invoked when client is created. Creates a client id and cache.
    Client can send messsages back to server, which are echo'd and displayed on client side.
    No more then 3 clients may exist at once.
    """

    #assigns a client id to the new client
    client_name = f"Client{client_id:02d}"

    #if more then three clients exist
    if len(clients) >= MAX_CLIENTS:
        client_socket.sendall(b"Server is full")
        client_socket.close()

    #if client successfully created, send client info to cache
    clients[client_name] = {"address": client_address, "connected_at": datetime.datetime.now()}

    #Display where client is connected from
    print(f"[NEW CONNECTION] {client_name} connected from {client_address}")

    #Notify client of it's name
    client_socket.sendall(client_name.encode())

    #server receiving messages from client
    try:
        while True:
            #receive message from client
            message = client_socket.recv(1024).decode().strip()

            if not message:
                break
            
            if message.lower() == "exit":
                break

            #if cache info is requested
            elif message.lower() == "status":

                #join dict info into a readable string
                status_message = "\n".join(
                    f"{name} connected at {info['connected_at']}" for name, info in clients.items()
                )
                client_socket.sendall(status_message.encode())

            #if file stream is requested
            elif message.lower() == "list":
                file_str = "\n"
                filepath = r'C:\Users\rmwc9\Documents\CP372 Programming Assignment\repo' #path to file repo
                file_list = os.listdir(filepath)

                if len(file_list) < 1:
                    client_socket.send("Repository contains no files".encode())
                
                else: #if repo is not empty
                    for file in file_list:
                        file_str += file + "\n"

                    #send list of files to client
                    client_socket.send(file_str.encode())
                    target = client_socket.recv(1024).decode()

                    #read contents of file
                    if target in file_list:
                        with open(os.path.join(filepath, target), "r") as file:
                            contents = file.read()

                        client_socket.send(contents.encode())
                    
                    else:
                        client_socket.send("File does not exist".encode())

            #if text is transmitted, eacho back to client after being acknowledged
            else:
                acked_message = message + "ACK"
                client_socket.sendall(acked_message.encode())

    except ConnectionResetError:
        print(f"[ERROR] {client_name} disconnected unexpectedly.")
    
    #When client is disconnected
    clients[client_name]["disconnected_at"] = datetime.datetime.now()

    print(f"[DISCONNECTED] {client_name} at {clients[client_name]['disconnected_at']}")

    del clients[client_name] #remove client from dictionary and free new spot for another client
    
    client_socket.close()


def start_server():
    """
    Function that starts the TCP server and invokes client creation method
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"[SERVER] Listening on {HOST}:{PORT}")

    client_id = 1

    #Invokes handle_client method, and creates a new client using threading
    while (True):
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, client_address, client_id)).start()
        client_id += 1

if __name__ == "__main__":
    start_server()