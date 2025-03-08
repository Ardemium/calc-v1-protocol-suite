import socket

def recv_all(sock: socket.socket, n: int) -> bytes:
    """
    Receive exactly n bytes from a socket.
    Returns the received bytes.
    """
    data = b''
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            break
        data += chunk
    return data
