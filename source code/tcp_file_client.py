"""
TCP File Client
Connects to TCP server and requests detailed file information
"""

import socket

def get_file_info_tcp(filename, host='127.0.0.1', port=9999):
    """
    Connect to TCP server and request file information
    """
    # Create TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Connect to the server
        print(f"[TCP Client] Connecting to {host}:{port}...")
        client_socket.connect((host, port))
        print("[TCP Client] Connected!")
        
        # Send filename request
        client_socket.send(filename.encode('utf-8'))
        
        # Receive response (up to 4096 bytes - files info can be bigger)
        data = client_socket.recv(4096)
        
        # Display response
        response = data.decode('utf-8')
        print(f"\n[TCP Client] Server response:\n{response}")
        return response
        
    except ConnectionRefusedError:
        print("[TCP Client] ERROR: Could not connect to server. Is it running?")
    except Exception as e:
        print(f"[TCP Client] ERROR: {e}")
    finally:
        client_socket.close()
        print("[TCP Client] Connection closed")

def main():
    """
    Interactive TCP client
    """
    print("=== TCP File Info Client ===")
    print("Enter filenames to get details, or 'quit' to exit")
    
    while True:
        filename = input("\nEnter filename: ").strip()
        
        if filename.lower() == 'quit':
            break
        
        if filename:
            get_file_info_tcp(filename)

if __name__ == "__main__":
    main()