import socket

def send_query(server_address, hostname, record_type):
    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Format the query
        query = f"{hostname} {record_type}"
        # Send query to server
        client_socket.sendto(query.encode(), server_address)
        # Receive response from server
        response, _ = client_socket.recvfrom(512)
        print(f"Received response: {response.decode()}")
    finally:
        client_socket.close()

def main():
    server_address = ('127.0.0.1', 8053)
    while True:
        hostname = input("Enter hostname to query: ")
        record_type = input("Enter record type (A/CNAME): ").strip().upper()
        send_query(server_address, hostname, record_type)
        cont = input("Do you want to query another hostname? (yes/no): ").strip().lower()
        if cont != 'yes':
            break

if __name__ == "__main__":
    main()

