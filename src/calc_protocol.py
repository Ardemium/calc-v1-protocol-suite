import struct
from typing import Tuple

class CalcProtocol:
    """
    Provides methods to pack and unpack calculator protocol messages with a metadata header.

    Metadata Header:
      - Magic Bytes: 4 bytes ("CALC")
      - Version: 1 byte (1)
    Header format: '!4sB' (total 5 bytes)

    Message types and payload formats:
      - Heartbeat:
          Payload: '!i16s' (4-byte int for message type, 16-byte string)
      - Operation Request:
          Payload: '!iBii' (4-byte int message type, 1-byte operator code,
                             4-byte int first operand, 4-byte int second operand)
      - Operation Response:
          Payload: '!iq' (4-byte int message type, 8-byte long integer result)
    """

    # Metadata constants
    METADATA_FORMAT: str = '!4sB'
    METADATA_SIZE: int = struct.calcsize(METADATA_FORMAT)
    MAGIC_BYTES: bytes = b'CALC'
    VERSION: int = 1

    # Heartbeat
    HEARTBEAT_PAYLOAD_FORMAT: str = '!i16s'
    HEARTBEAT_PAYLOAD_SIZE: int = struct.calcsize(HEARTBEAT_PAYLOAD_FORMAT)
    HEARTBEAT_TOTAL_SIZE: int = METADATA_SIZE + HEARTBEAT_PAYLOAD_SIZE

    # Operation Request
    OP_REQ_PAYLOAD_FORMAT: str = '!iBii'
    OP_REQ_PAYLOAD_SIZE: int = struct.calcsize(OP_REQ_PAYLOAD_FORMAT)
    OP_REQ_TOTAL_SIZE: int = METADATA_SIZE + OP_REQ_PAYLOAD_SIZE

    # Operation Response
    OP_RESP_PAYLOAD_FORMAT: str = '!iq'
    OP_RESP_PAYLOAD_SIZE: int = struct.calcsize(OP_RESP_PAYLOAD_FORMAT)
    OP_RESP_TOTAL_SIZE: int = METADATA_SIZE + OP_RESP_PAYLOAD_SIZE

    @classmethod
    def pack_header(cls) -> bytes:
        """
        Pack the metadata header.
        """
        return struct.pack(cls.METADATA_FORMAT, cls.MAGIC_BYTES, cls.VERSION)

    @classmethod
    def unpack_header(cls, data: bytes) -> Tuple[bytes, int]:
        """
        Unpack the metadata header.
        Returns a tuple: (magic_bytes, version).
        """
        return struct.unpack(cls.METADATA_FORMAT, data)

    @classmethod
    def pack_heartbeat(cls, message_type: int, text: str) -> bytes:
        """
        Pack a heartbeat message with metadata.
        """
        encoded = text.encode('utf-8')[:16]
        padded = encoded.ljust(16, b'\x00')
        payload = struct.pack(cls.HEARTBEAT_PAYLOAD_FORMAT, message_type, padded)
        header = cls.pack_header()
        return header + payload

    @classmethod
    def unpack_heartbeat(cls, data: bytes) -> Tuple[int, str]:
        """
        Unpack a heartbeat message.
        Returns a tuple: (message_type, text).
        Raises ValueError if the header is invalid.
        """
        header = data[:cls.METADATA_SIZE]
        payload = data[cls.METADATA_SIZE: cls.METADATA_SIZE + cls.HEARTBEAT_PAYLOAD_SIZE]
        magic, version = cls.unpack_header(header)
        if magic != cls.MAGIC_BYTES or version != cls.VERSION:
            raise ValueError("Invalid header")
        msg_type, raw_text = struct.unpack(cls.HEARTBEAT_PAYLOAD_FORMAT, payload)
        text = raw_text.rstrip(b'\x00').decode('utf-8')
        return msg_type, text

    @classmethod
    def pack_operation_request(cls, message_type: int, op_code: int, num1: int, num2: int) -> bytes:
        """
        Pack an operation request message with metadata.
        """
        payload = struct.pack(cls.OP_REQ_PAYLOAD_FORMAT, message_type, op_code, num1, num2)
        header = cls.pack_header()
        return header + payload

    @classmethod
    def unpack_operation_request(cls, data: bytes) -> Tuple[int, int, int, int]:
        """
        Unpack an operation request message.
        Returns a tuple: (message_type, op_code, num1, num2).
        Raises ValueError if the header is invalid.
        """
        header = data[:cls.METADATA_SIZE]
        payload = data[cls.METADATA_SIZE: cls.METADATA_SIZE + cls.OP_REQ_PAYLOAD_SIZE]
        magic, version = cls.unpack_header(header)
        if magic != cls.MAGIC_BYTES or version != cls.VERSION:
            raise ValueError("Invalid header")
        return struct.unpack(cls.OP_REQ_PAYLOAD_FORMAT, payload)

    @classmethod
    def pack_operation_response(cls, message_type: int, result: int) -> bytes:
        """
        Pack an operation response message with metadata.
        """
        payload = struct.pack(cls.OP_RESP_PAYLOAD_FORMAT, message_type, result)
        header = cls.pack_header()
        return header + payload

    @classmethod
    def unpack_operation_response(cls, data: bytes) -> Tuple[int, int]:
        """
        Unpack an operation response message.
        Returns a tuple: (message_type, result).
        Raises ValueError if the header is invalid.
        """
        header = data[:cls.METADATA_SIZE]
        payload = data[cls.METADATA_SIZE: cls.METADATA_SIZE + cls.OP_RESP_PAYLOAD_SIZE]
        magic, version = cls.unpack_header(header)
        if magic != cls.MAGIC_BYTES or version != cls.VERSION:
            raise ValueError("Invalid header")
        return struct.unpack(cls.OP_RESP_PAYLOAD_FORMAT, payload)
