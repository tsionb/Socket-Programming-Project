"""
TCP File Server
Provides detailed file information to connected clients
Handles multiple clients using threading
"""

import socket
import threading
import os
import time
from datetime import datetime

def handle_client(client_socket, address):
    """
    Handle a single TCP client connection
    Each client runs in its own thread
    """
    print(f"[TCP Server] New connection from {address}")
    
    try:
        while True:
            # Receive client request (up to 1024 bytes)
            data = client_socket.recv(1024)
            
            if not data:
                # No data means client closed connection
                break
            
            # Decode the request
            filename = data.decode('utf-8').strip()
            print(f"[TCP Server] Request from {address}: '{filename}'")
            
            # Generate detailed file information
            if os.path.isfile(filename):
                # Get file stats
                stats = os.stat(filename)
                
                # Format file information
                response = f"""
FILE INFORMATION: {filename}
-------------------
Size: {stats.st_size} bytes
Created: {datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}
Modified: {datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
Permissions: {oct(stats.st_mode)[-3:]}
                """
            else:
                response = f"ERROR: File '{filename}' not found"
            
            # Send response back to client
            client_socket.send(response.encode('utf-8'))
            
    except Exception as e:
        print(f"[TCP Server] Error with {address}: {e}")
    finally:
        print(f"[TCP Server] Closing connection to {address}")
        client_socket.close()

def run_tcp_server(host='127.0.0.1', port=9999):
    """
    Main TCP server that listens for connections and spawns threads
    """
    # Create TCP socket (SOCK_STREAM = TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Allow reusing the address (helps when restarting server)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to address and port
    server_socket.bind((host, port))
    
    # Listen for connections (max 5 clients in queue)
    server_socket.listen(5)
    print(f"[TCP Server] Listening on {host}:{port}")
    print("[TCP Server] Ready to accept connections...")
    
    try:
        while True:
            # Accept new connection (blocks until client connects)
            client_socket, address = server_socket.accept()
            
            # Create a new thread to handle this client
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address)
            )
            client_thread.daemon = True  # Thread dies when main dies
            client_thread.start()
            
            print(f"[TCP Server] Active connections: {threading.active_count() - 1}")
            
    except KeyboardInterrupt:
        print("\n[TCP Server] Shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_tcp_server()