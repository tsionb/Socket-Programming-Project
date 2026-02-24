"""
Main Application Controller
Unified interface for running servers or clients with both protocols
"""

import argparse
import threading
import time
import os

# Import our modules
import udp_file_server
import udp_file_client
import tcp_file_server
import tcp_file_client

def run_all_servers():
    """
    Run both UDP and TCP servers in separate threads
    """
    print("=" * 50)
    print("Starting File Metadata Servers")
    print("=" * 50)
    print("Press Ctrl+C to stop all servers\n")
    
    # Create threads for each server
    udp_thread = threading.Thread(
        target=udp_file_server.run_udp_server,
        args=('127.0.0.1', 8888),
        daemon=True
    )
    
    tcp_thread = threading.Thread(
        target=tcp_file_server.run_tcp_server,
        args=('127.0.0.1', 9999),
        daemon=True
    )
    
    # Start servers
    udp_thread.start()
    time.sleep(1)  # Small delay so UDP can start first
    tcp_thread.start()
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nShutting down all servers...")

def run_client_mode():
    """
    Interactive client that can use either protocol
    """
    print("=" * 50)
    print("File Metadata Client")
    print("=" * 50)
    print("Commands:")
    print("  udp <filename>  - Quick check via UDP (fast)")
    print("  tcp <filename>  - Detailed info via TCP (reliable)")
    print("  quit            - Exit client")
    print()
    
    while True:
        command = input(">> ").strip()
        
        if command.lower() == 'quit':
            break
        
        if command.startswith('udp '):
            filename = command[4:].strip()
            if filename:
                print(f"\n[UDP Query] Checking '{filename}'...")
                udp_file_client.query_udp_server(filename)
            else:
                print("Please specify a filename")
                
        elif command.startswith('tcp '):
            filename = command[4:].strip()
            if filename:
                print(f"\n[TCP Query] Getting details for '{filename}'...")
                tcp_file_client.get_file_info_tcp(filename)
            else:
                print("Please specify a filename")
        else:
            print("Unknown command. Use: udp <file> or tcp <file>")

def create_sample_files():
    """
    Create some sample files for testing
    """
    print("Creating sample files for testing...")
    
    sample_files = {
        "test1.txt": "This is a test file.\nIt has multiple lines.\nFor testing purposes.",
        "test2.txt": "Another test file with different content.",
        "data.txt": "Sample data file with some numbers:\n42\n123\n789",
    }
    
    for filename, content in sample_files.items():
        with open(filename, 'w') as f:
            f.write(content)
        print(f"  Created: {filename}")
    
    print("\nSample files ready!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Metadata Application')
    parser.add_argument('mode', choices=['server', 'client', 'test'],
                       help='Run as server, client, or create test files')
    
    args = parser.parse_args()
    
    if args.mode == 'server':
        run_all_servers()
    elif args.mode == 'client':
        run_client_mode()
    elif args.mode == 'test':
        create_sample_files()