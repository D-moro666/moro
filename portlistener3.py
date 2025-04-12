import socket
import ssl
import threading


def listen_on_port(port, ssl_context):
    try:
        # Create a socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", port))  # Bind to all interfaces
        server_socket.listen(5)
        print(f"Listening with SSL on port {port}...")

        # Wrap the socket with SSL
        secure_socket = ssl_context.wrap_socket(server_socket, server_side=True)

        while True:
            client_socket, address = secure_socket.accept()
            print(f"Secure connection received on port {port} from {address}")
            client_socket.close()

    except Exception as e:
        print(f"Error on port {port}: {e}")


def start_listeners(port_range, ssl_context):
    threads = []
    for port in port_range:
        thread = threading.Thread(target=listen_on_port, args=(port, ssl_context))
        thread.daemon = True  # This closes the thread when the program exits
        threads.append(thread)
        thread.start()

    # Keep the main thread running
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    # Define the path to your SSL certificate and key files
    ssl_cert_file = "C:/nginx-1.27.4/conf/Mohamed.crt"
    ssl_key_file = "C:/nginx-1.27.4/conf/Mohamed.key"

    # Define the range of ports you want to monitor
    port_range = range(1, 65535)  # Example: Change this to the range you need

    # Create a SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile=ssl_cert_file, keyfile=ssl_key_file)

    # Start listening on ports with SSL
    start_listeners(port_range, ssl_context)
