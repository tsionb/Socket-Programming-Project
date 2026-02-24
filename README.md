# Socket Programming Project: File Metadata Server

## 1. Project Overview

This project implements a client-server application that provides file metadata services using both UDP and TCP protocols. Users can query file existence (UDP) or retrieve detailed file information (TCP) from a remote server.

### Why This Application?
- Demonstrates both UDP and TCP in a practical context
- Shows the trade-offs between speed (UDP) and reliability/detail (TCP)
- Implements real-world functionality (file information retrieval)

## 2. Protocol Design

### UDP Protocol
- **Type**: Connectionless, unreliable
- **Port**: 8888
- **Message Format**: Plain text filename
- **Response Format**: "YES: [details]" or "NO: [details]"
- **Use Case**: Quick existence checks where occasional loss is acceptable

### TCP Protocol
- **Type**: Connection-oriented, reliable
- **Port**: 9999
- **Message Format**: Plain text filename
- **Response Format**: Multi-line formatted file information
- **Use Case**: Detailed file info where reliability matters

## 3. Implementation Details

### Architecture
- **UDP Server**: Single-threaded, handles one query at a time
- **TCP Server**: Multi-threaded, handles multiple clients simultaneously
- **Clients**: Interactive command-line interfaces

### Key Code Snippets

**UDP Socket Creation**:
```python
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

**TCP Socket Creation**:
```python
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

**Multi-threading TCP**:
```python
client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
client_thread.start()

## 4. How to Run

 **Prerequisites**:

- Python 3.6 or higher
- No external libraries required (uses standard library only)

**Running the Servers**:
```bash
python file_metadata_app.py server

**Running the Client**:
```bash
python file_metadata_app.py client

**Using Executables**:
- Navigate to the dist folder
- Run file_metadata.exe 

## 5. Testing Results

**UDP Test**:
```text
Client query: "test1.txt"
Server response: "YES: File 'test1.txt' exists"
Response time: ~1ms

**TCP Test**:
```text
Client query: "test1.txt"
Server response:
FILE INFORMATION: test1.txt
-------------------
Size: 67 bytes
Created: 2026-02-24 05:43:49
Modified: 2026-02-24 05:43:49
Permissions: 665

**Multiple TCP Clients**:

- Tested with 5 simultaneous clients
- All received correct responses
- Server maintained stability