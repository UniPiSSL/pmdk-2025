import socket
import threading

def handle_connection(client_socket, port):
    # This is just a placeholder to keep the connection alive and the port open
    print(f"Handling connection on port {port}...")
    client_socket.send(f"Welcome to port {port}!\n".encode())  # Just send a message to the client
    client_socket.close()

def open_ports_from_string(input_string):
    ports = []

    def open_port(port):
        try:
            # Open a TCP socket and listen on the port
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('0.0.0.0', port))
            s.listen(5)
            print(f"Port {port} opened.")
            ports.append(port)
            
            # Accept incoming connections in a separate thread
            while True:
                client_socket, addr = s.accept()
                threading.Thread(target=handle_connection, args=(client_socket, port)).start()
        except Exception as e:
            print(f"Failed to open port {port}. Error: {e}")

    # Iterate over each character in the string and open corresponding port
    for char in input_string:
        ascii_value = ord(char)
        threading.Thread(target=open_port, args=(ascii_value,)).start()

    return ports

if __name__ == '__main__':
    flag = b"FLAG{5n34ky_p027_3xf1lt24710n}".hex()
    input_string = flag
    opened_ports = open_ports_from_string(input_string)
    print(f"Ports opened: {opened_ports}")
