# Discordn-t
# Discordn't - A Simple TCP Chat Room

Discordn't is a lightweight chat server implemented in raw Python using TCP sockets. Designed as part of a school assignment, the project explores low-level networking by simulating a minimal chat API server over TCP, mimicking basic HTTP behavior without relying on web frameworks like Flask or Django.

## 🚀 Features

- 📩 `POST /api/messages`: Append messages to a log file (`chat_log.txt`)
- 📜 `GET /api/messages`: Retrieve all messages from the log
- 📄 Simulated HTTP-like request handling over raw TCP
- 🧼 Clean, minimal implementation (under 100 lines of code)
- 🎓 Educational value — helps understand how HTTP and web servers work at the socket level

## 🧠 Why This Project?

This project was a class assignment aimed at building a deeper understanding of how servers work at a low level. Instead of using higher-level abstractions, it uses Python’s `socket` module directly to:

- Accept and respond to raw TCP connections
- Handle simple HTTP-style requests
- Process routing logic based on method and URL

This helped reinforce key concepts such as:

- TCP connection handling
- Request parsing
- State persistence via file I/O
- Statelessness in server design

## 🛠️ How It Works

### Server Behavior

- Listens for TCP connections on port `50001`
- Accepts requests with a first-line format like `POST /api/messages` or `GET /api/messages`
- Parses the request manually to extract method, path, and body
- Routes the request to appropriate handler functions
- Sends a plain response back to the client (text, not HTTP-formatted)

### Endpoints

| Method | Path             | Description                          |
|--------|------------------|--------------------------------------|
| GET    | `/api/messages`  | Returns contents of `chat_log.txt`   |
| POST   | `/api/messages`  | Appends a message to `chat_log.txt`  |

## 📁 File Overview

- `server.py`: Main TCP server logic for handling chat requests
- `chat_log.txt`: Stores messages sent by clients
- `webserver.py` (optional): Experimental HTTP file server serving `index.html` on port `8080`

## 📦 Requirements

- Python 3.x
- No third-party dependencies


