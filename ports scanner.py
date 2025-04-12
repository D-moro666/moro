import socket
import ssl
import threading
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# General-purpose listener function with SSL support as optional
def listen_on_port(port, ssl_context=None):
    try:
        # Create the socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", port))  # Bind to all interfaces
        server_socket.listen(5)
buildctl --addr unix:///tmp/buildkitd.sock debug workers
        if ssl_context:
            logging.info(f"SSL server is securely listening on port {port}...")
            server_socket = ssl_context.wrap_socket(server_socket, server_side=True)
        else:
            logging.info(f"Non-SSL server is listening on port {port}...")

        # Accept connections
        while True:
            try:
                client_socket, address = server_socket.accept()
                logging.info(f"New connection from {address} on port {port}")

                # Simple HTTP response
                try:
                    request = client_socket.recv(1024).decode('utf-8')
                    logging.debug(f"Request received on port {port}: {request}")

                    # Send a basic response
                    if ssl_context:
                        client_socket.sendall(
                            b"HTTP/1.1 200 OK\r\n"
                            b"Content-Type: text/plain\r\n"
                            b"Content-Length: 20\r\n"
                            b"\r\n"
                            b"Hello from SSL Port!"
                        )
                    else:
                        client_socket.sendall(
                            b"HTTP/1.1 200 OK\r\n"
                            b"Content-Type: text/plain\r\n"
                            b"Content-Length: 21\r\n"
                            b"\r\n"
                            b"Hello from Non-SSL Port!"
                        )
                except Exception as client_error:
                    logging.error(f"Error handling client request on port {port}: {client_error}")
                finally:
                    client_socket.close()

            except ssl.SSLError as ssl_error:
                logging.error(f"SSL handshake error on port {port}: {ssl_error}")
            except Exception as e:
                logging.error(f"General error on port {port}: {e}")

    except Exception as e:
        logging.critical(f"Critical error on port {port}: {e}")
    finally:
        server_socket.close()
        logging.info(f"Server on port {port} has been shut down.")


if __name__ == "__main__":
    # Define SSL-related paths
    ssl_cert_file = "C:/nginx-1.27.4/conf/Mohamed.crt"  # Replace with your certificate path
    ssl_key_file = "C:/nginx-1.27.4/conf/Mohamed.key"  # Replace with your key path

    try:
        # Create the SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile=ssl_cert_file, keyfile=ssl_key_file)
        ssl_context.options |= ssl.OP_NO_SSLv2  # Disable SSLv2
        ssl_context.options |= ssl.OP_NO_SSLv3  # Disable SSLv3
        ssl_context.options |= ssl.OP_NO_TLSv1  # Disable TLSv1
        ssl_context.options |= ssl.OP_NO_TLSv1_1  # Disable TLSv1.1
        ssl_context.set_ciphers("HIGH:!aNULL:!MD5")
        logging.info("SSL context initialized successfully.")

        # Start multiple servers
        ports_to_listen = [
            (443, ssl_context),  # HTTPS port with SSL
            (8443, ssl_context),  # Another SSL port (if needed)
            (80, None),  # HTTP port without SSL
            (8080, None)  # HTTP alternative port
        ]

        threads = []
        for port, context in ports_to_listen:
            thread = threading.Thread(target=listen_on_port, args=(port, context))
            thread.daemon = True  # Allow threads to exit when the main program exits
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except FileNotFoundError as fnf_error:
        logging.critical(f"SSL certificate or key file not found: {fnf_error}")
    except ssl.SSLError as ssl_error:
        logging.critical(f"SSL context setup failed: {ssl_error}")
    except Exception as e:
        logging.critical(f"Critical setup error: {e}")
