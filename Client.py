"""
CP372 Programming Assignment
Ryan Chisholm - Michael Wu
February 10th 2025

Client side source code
"""
import socket

HOST = "127.0.0.1"
PORT = 12345

def start_client():
    """
    Initializes the client when invoked.
    Takes input and can perform multiple operations such as ask for cache info, send messages or terminate.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    message = client_socket.recv(1024).decode()

    #If server already has 3 clients, close socket and terminate
    if(message == "Server is full"):
        client_socket.close()
        quit()
    
    #Receive assigned name from server
    client_name = message
    print(f"Connected as {client_name}")

    #Sending messages to the server
    try:
        while True:
            message = input("> Enter message (or 'exit' to quit, 'status' for client information) ")

            #if 'exit' is sent
            if message.lower() == "exit":
                client_socket.sendall(b"exit")
                break

            #if 'list' is sent
            elif message.lower() == "list":
                client_socket.send(message.encode()) #requsts list of files
                list = client_socket.recv(1024).decode() #receives list of files
                print('File List: ', list)

                if list == 'Repository contains no files': #if repo is empty
                    continue

                choice = input('Enter the name of file to stream: ') #enter name of file to read
                client_socket.send(choice.encode()) #sends file choice to server
                chosen = client_socket.recv(1024).decode() #receive's file data from server
                print(chosen)

            #send message to server, and then receive back
            else:
                client_socket.sendall(message.encode())
                print(client_socket.recv(1024).decode())

    except KeyboardInterrupt:
        print("\n[CLIENT] Exiting...")

    #close client after it disconnects
    client_socket.close()

if __name__ == "__main__":
    start_client()
