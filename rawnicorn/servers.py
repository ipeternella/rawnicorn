"""
Some iunicorn server implementations.
"""
import socket


class RawnicornBlocking:
    def start(self, ip, port):
        sock = socket.socket()  # AF_INET socket
        sock.bind((ip, port))  # bind to (ip, port) address
        sock.listen(5)  # backlog of conns before refusing new ones
        sock_address = sock.getsockname()  # tuple (ip, port) for TCP-based sockets

        try:
            print(f"Listening to connections on {sock_address}")

            while True:
                remote_sock, remote_sock_addr = sock.accept()  # accepts a connection from the remote (cli) socket
                print(f"Accepted connection from: {remote_sock_addr}")

                buffer_data = remote_sock.recv(1024)  # read from network buffer, returns when buffer is full

                while buffer_data:  # while buffer_data != b''

                    print(f"Received bytes: {buffer_data.decode('utf-8')}\n")
                    buffer_data = remote_sock.recv(1024)

                print("done!")

        except KeyboardInterrupt:
            sock.close
