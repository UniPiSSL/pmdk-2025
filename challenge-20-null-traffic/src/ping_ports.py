import socket

def get_ports(string):
    p = []
    for char in string:
        ascii_value = ord(char)
        p.append(ascii_value)
    return p

def ping_ports(ports):
    for port in ports:
        try:
            # Attempt to connect to the port
            with socket.create_connection(('127.0.0.1', port), timeout=1) as s:
                print(f"Port {port} is open (ping successful).")
        except (socket.timeout, ConnectionRefusedError):
            print(f"Port {port} is closed (ping failed).")

if __name__ == '__main__':
    # Example list of ports based on ASCII from previous script (could be taken from a file, etc.)
    flag = b"FLAG{5n34ky_p027_3xf1lt24710n}".hex()
    input_string = flag
    ports = get_ports(input_string)
    ping_ports(ports)
