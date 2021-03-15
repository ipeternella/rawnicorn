"""
Some client sockets.
"""
import errno
import select
import socket


def send_until_completion(sock: socket.socket, data: str):
    total_transferred_bytes = 0
    total_transfer_bytes = len(data)
    data_cursor = data.encode("utf-8")  # encode to bytes

    print(f"Starting transfer of {total_transfer_bytes} bytes...")

    while total_transferred_bytes < total_transfer_bytes:
        try:
            transferred_bytes = sock.send(data_cursor)
            print(f"transferred some chunk: {transferred_bytes}")
        except OSError as e:
            if e.errno != errno.EAGAIN:
                raise e
            # write buffer may be full (not consumed yet by client), so EAGAIN is raised to try again
            print("Write buffer is still full, retrying...")

            # invokes OS polling file descriptor API for to continue once socket's ready for writing again
            select.select([], [sock], [])

        total_transferred_bytes += transferred_bytes
        data_cursor = data_cursor[transferred_bytes:]  # move the cursor for next chunk transfer


def send(host: str, port: int, data: str, blocking=True) -> str:

    TCP_SOCKET_TYPE = socket.SOCK_STREAM
    IPV4_SOCKET_FAMILY = socket.AF_INET

    with socket.socket(IPV4_SOCKET_FAMILY, TCP_SOCKET_TYPE) as sock:
        print(f"Connecting to {host}:{port}...")
        sock.connect((host, port))

        print("Configuring client socket...")
        sock.setblocking(blocking)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024)  # write buffer size

        print("Writing to the socket's write buffer...")

        if blocking:
            data_bytes_array = data.encode("utf-8")  # encode str, using utf-8, to bytes
            sock.send(data_bytes_array)
        else:
            send_until_completion(sock, data)

    return data


if __name__ == "__main__":
    data = "-" * 1024 * 8

    send("localhost", 8080, data, blocking=False)
