"""
UDP File Server
Listens for file existence queries and responds via UDP
"""

import socket
import os

def run_udp_server(host='127.0.0.1', port=8888):
    """
    UDP Server that checks if files exist on the server
    """
    # Create a UDP socket
    # AF_INET = IPv4, SOCK_DGRAM = UDP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the address and port
    server_socket.bind((host, port))
    print(f"[UDP Server] Listening on {host}:{port}")
    
    try:
        while True:
            # Receive data from client (up to 1024 bytes)
            # recvfrom returns (data, client_address)
            data, client_address = server_socket.recvfrom(1024)
            
            # Decode the received message (it's bytes, need to decode to string)
            filename = data.decode('utf-8').strip()
            print(f"[UDP Server] Received query for: '{filename}' from {client_address}")
            
            # Check if file exists in current directory
            if os.path.isfile(filename):
                response = f"YES: File '{filename}' exists"
            else:
                response = f"NO: File '{filename}' not found"
            
            # Send response back to client
            server_socket.sendto(response.encode('utf-8'), client_address)
            print(f"[UDP Server] Sent response: {response}")
            
    except KeyboardInterrupt:
        print("\n[UDP Server] Shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    run_udp_server()