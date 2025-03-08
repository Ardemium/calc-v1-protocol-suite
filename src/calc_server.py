import socket
import threading
import logging
from calc_protocol import CalcProtocol
from network_utils import recv_all

HOST = '127.0.0.1'
PORT = 6000

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

def perform_operation(op_code: int, num1: int, num2: int) -> int:
    """
    Perform an arithmetic operation on two integers.
    Uses integer division for division.
    """
    if op_code == 1:
        return num1 + num2
    elif op_code == 2:
        return num1 - num2
    elif op_code == 3:
        return num1 * num2
    elif op_code == 4:
        if num2 == 0:
            return 0
        return num1 // num2
    return 0

def handle_client(conn: socket.socket, addr: tuple) -> None:
    logging.info("Connected by %s", addr)
    try:
        # Receive heartbeat message.
        heartbeat_data = recv_all(conn, CalcProtocol.HEARTBEAT_TOTAL_SIZE)
        if len(heartbeat_data) != CalcProtocol.HEARTBEAT_TOTAL_SIZE:
            conn.close()
            return

        msg_type, text = CalcProtocol.unpack_heartbeat(heartbeat_data)
        if msg_type != 0 or text.lower() != "hello":
            conn.close()
            return

        # Send heartbeat response.
        response = CalcProtocol.pack_heartbeat(0, "helo world")
        conn.sendall(response)

        # Receive operation request.
        op_req_data = recv_all(conn, CalcProtocol.OP_REQ_TOTAL_SIZE)
        if len(op_req_data) != CalcProtocol.OP_REQ_TOTAL_SIZE:
            conn.close()
            return

        req_msg_type, op_code, num1, num2 = CalcProtocol.unpack_operation_request(op_req_data)
        if req_msg_type != 1:
            conn.close()
            return

        result = perform_operation(op_code, num1, num2)
        op_resp_data = CalcProtocol.pack_operation_response(1, result)
        conn.sendall(op_resp_data)
    except Exception as error:
        logging.error("Error with client %s: %s", addr, error)
    finally:
        conn.close()
        logging.info("Closed connection to %s", addr)

def start_server(host: str = HOST, port: int = PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
        logging.info("Server running on %s:%d", host, port)
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
