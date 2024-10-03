import socket

# Define a dictionary to hold DNS records
dns_records = {
    'example.com': {'type': 'A', 'value': '93.184.216.34'},
    'alias.com': {'type': 'CNAME', 'value': 'example.com'},
    'google.com': {'type': 'A', 'value': '8.8.8.8'},
    'alias2.com': {'type': 'CNAME', 'value': 'google.com'}
}

def handle_query(data):
    # Decode the query
    query = data.decode().strip()
    print(f"Received query: {query}")

    # Split the query to get hostname and record type
    parts = query.split()
    if len(parts) != 2:
        return "Invalid query format. Use: <hostname> <type>".encode()
    
    hostname, record_type = parts

    # Check if hostname is in DNS records
    if hostname in dns_records:
        record = dns_records[hostname]
        if record['type'] == record_type:
            response = f"{hostname} -> {record['value']}"
            # If it's a CNAME, resolve it to its final A record
            if record_type == 'CNAME' and record['value'] in dns_records:
                cname_record = dns_records[record['value']]
                if cname_record['type'] == 'A':
                    response += f" -> {cname_record['value']}"
        else:
            response = f"No {record_type} record found for {hostname}"
    else:
        response = f"{hostname} not found"

    return response.encode()

def start_dns_server(host='127.0.0.1', port=8053):
    # Create a UDP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print("DNS server is running on port 8053...")

    while True:
        # Receive data from client
        data, client_address = server_socket.recvfrom(512)
        response = handle_query(data)
        # Send response back to client
        server_socket.sendto(response, client_address)

if __name__ == "__main__":
    start_dns_server()

