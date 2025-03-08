import socket
import logging
from calc_protocol import CalcProtocol
from network_utils import recv_all

HOST = '127.0.0.1'
PORT = 6000

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

def start_client(host: str = HOST, port: int = PORT) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((host, port))
        logging.info("Connected to %s:%d", host, port)
        try:
            # Send heartbeat request.
            heartbeat_msg = CalcProtocol.pack_heartbeat(0, "hello")
            client_socket.sendall(heartbeat_msg)

            # Receive heartbeat response.
            hb_response = recv_all(client_socket, CalcProtocol.HEARTBEAT_TOTAL_SIZE)
            if len(hb_response) != CalcProtocol.HEARTBEAT_TOTAL_SIZE:
                return
            resp_msg_type, resp_text = CalcProtocol.unpack_heartbeat(hb_response)
            if resp_msg_type != 0 or resp_text.lower() != "helo world":
                return

            # Input operation parameters.
            op_code = int(input("Enter operation code (1: add, 2: subtract, 3: multiply, 4: divide): "))
            num1 = int(input("Enter first integer: "))
            num2 = int(input("Enter second integer: "))

            # Send operation request.
            op_req_msg = CalcProtocol.pack_operation_request(1, op_code, num1, num2)
            client_socket.sendall(op_req_msg)

            # Receive operation response.
            op_resp = recv_all(client_socket, CalcProtocol.OP_RESP_TOTAL_SIZE)
            if len(op_resp) != CalcProtocol.OP_RESP_TOTAL_SIZE:
                return
            resp_msg_type, result = CalcProtocol.unpack_operation_response(op_resp)
            logging.info("Operation result: %d", result)
        except Exception as error:
            logging.error("Client error: %s", error)

if __name__ == "__main__":
    start_client()
