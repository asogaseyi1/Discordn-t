import socket
import json

HOST = ''  # Listen on all available interfaces
WEB_PORT = 50001  # Port for web server requests
BUFFER_SIZE = 1024  # Size of message chunks to receive

def save_message_to_file(message):
    # Append the message with a newline to separate messages
    with open("chat_log.txt", "a") as f:
        f.write(message + "\n")

def get_messages_from_file():
    # Return all messages as a list of strings
    try:
        with open("chat_log.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""  # Return empty string if file not found

def handle_request(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE).decode()
        headers, body = request.split('\r\n\r\n', 1)
        request_line = headers.split('\r\n')[0]
        method, path, _ = request_line.split()
        
        if path == "/api/messages" and method == "GET":
            messages = get_messages_from_file().splitlines()
            response_body = json.dumps(messages)
            client_socket.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: {len(response_body)}\r\n\r\n{response_body}".encode())
        elif path == "/api/messages" and method == "POST":
            save_message_to_file(body.strip())  # Assume the body is the raw message text
            client_socket.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage saved")
        else:
            client_socket.sendall(b"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\nPage not found")
    finally:
        client_socket.close()

def setup_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, WEB_PORT))
    server_socket.listen(5)
    print(f"Server started on port {WEB_PORT} for web API")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr}")
        handle_request(client_socket)

if __name__ == "__main__":
    setup_server()