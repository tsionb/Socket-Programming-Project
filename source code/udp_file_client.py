"""
UDP File Client
Sends file existence queries to UDP server and waits for response
"""

import socket

def query_udp_server(filename, host='127.0.0.1', port=8888):
    """
    Send a UDP query to check if a file exists
    """
    # Create UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Set a timeout so we don't wait forever if server doesn't respond
    client_socket.settimeout(3.0)
    
    try:
        # Send the filename to the server
        print(f"[UDP Client] Asking about file: '{filename}'")
        client_socket.sendto(filename.encode('utf-8'), (host, port))
        
        # Wait for response (up to 1024 bytes)
        data, server_address = client_socket.recvfrom(1024)
        
        # Decode and display response
        response = data.decode('utf-8')
        print(f"[UDP Client] Server response: {response}")
        return response
        
    except socket.timeout:
        print("[UDP Client] ERROR: No response from server (timeout)")
        return "ERROR: Server timeout"
    except Exception as e:
        print(f"[UDP Client] ERROR: {e}")
        return f"ERROR: {e}"
    finally:
        client_socket.close()

def main():
    """
    Interactive UDP client
    """
    print("=== UDP File Query Client ===")
    print("Enter filenames to check, or 'quit' to exit")
    
    while True:
        filename = input("\nEnter filename: ").strip()
        
        if filename.lower() == 'quit':
            break
        
        if filename:
            query_udp_server(filename)

if __name__ == "__main__":
    main()