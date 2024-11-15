import socket
import threading
import os

HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = 8080       # Web server port
CHAT_SERVER_HOST = 'localhost'
CHAT_SERVER_PORT = 50001  # Port of the chat server
BUFFER_SIZE = 1024

def send_response(client_socket, status_code, content_type, body):
    body = body.encode('utf-8')  # Ensure body is bytes
    response = f"HTTP/1.1 {status_code}\r\nContent-Type: {content_type}\r\nContent-Length: {len(body)}\r\n\r\n"
    client_socket.sendall(response.encode('utf-8') + body)

def serve_static_file(client_socket, path):
    if path == "/":
        path = "/index.html"  # Default to index.html

    try:
        with open("." + path, 'rb') as f:
            body = f.read()
            content_type = "text/html" if path.endswith(".html") else "text/javascript"
            send_response(client_socket, "200 OK", content_type, body.decode('utf-8'))
    except FileNotFoundError:
        send_response(client_socket, "404 Not Found", "text/html", "<h1>404 Not Found</h1>")

def chat_server_request(method, endpoint, data=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as chat_socket:
        chat_socket.connect((CHAT_SERVER_HOST, CHAT_SERVER_PORT))
        request = f"{method} {endpoint} HTTP/1.1\r\nContent-Length: {len(data) if data else 0}\r\n\r\n"
        if data:
            request += data
        chat_socket.sendall(request.encode())

        # Read the full response including headers
        response = b""
        while True:
            part = chat_socket.recv(BUFFER_SIZE)
            response += part
            if len(part) < BUFFER_SIZE:
                break

        response_str = response.decode()
        headers, body = response_str.split("\r\n\r\n", 1)
        return body

def handle_client(client_socket):
    request = client_socket.recv(BUFFER_SIZE).decode('utf-8')
    headers, body = request.split('\r\n\r\n', 1)
    request_line = headers.split('\r\n')[0]
    method, path, _ = request_line.split()
    
    if path.startswith("/api/"):
        response = chat_server_request(method, path, body)
        send_response(client_socket, "200 OK", "text/plain", response)
    else:
        serve_static_file(client_socket, path)

    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Web server started on port {PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
