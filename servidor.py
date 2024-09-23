import socket
import threading

def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Mensaje recibido de {client_address}: {message}")
                broadcast(f"{client_address}: {message}", client_socket)
        except:
            remove_client(client_socket)
            break

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket: ## el mensaje solo se envia a los clientes que no son el sender
            try:
                client.send(message.encode())
            except:
                remove_client(client)

def remove_client(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

clients = set()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('172.28.255.7', 5000))
    server.listen(5)
    print("Servidor iniciado en localhost:5000")

    while True:
        client_socket, client_address = server.accept()
        clients.add(client_socket)
        print(f"Nueva conexión de {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        # hilo que maneja el cliente
        client_thread.start()

if __name__ == "__main__":
    start_server()