# Client-Server Calculator Protocol

## Overview

This project implements a client-server calculator that uses a custom binary protocol over TCP sockets in Python. The client sends two 32-bit integers and an operator code to the server. The server performs the arithmetic operation and returns the result as a 64-bit integer. A heartbeat message verifies that the server is available before the operation request. Each message includes a fixed metadata header.

## Protocol Metadata

Every message begins with a metadata header that contains the protocol identifier and version. The header has the following structure:

- **Magic Bytes (4 bytes):** The fixed value `CALC` (in ASCII) to identify the protocol.
- **Version (1 byte):** The protocol version number (currently `1`).

The header is prepended to every message.

## Protocol Specification

### Metadata Header

- **Format:** `!4sB` (4-byte string and 1-byte unsigned integer)
- **Size:** 5 bytes
- **Values:**
  - Magic Bytes: `"CALC"`
  - Version: `1`

### Heartbeat Message

- **Purpose:** Verify server availability.
- **Payload Format:** `!i16s`
  - 4-byte integer: Message type (`0` for heartbeat).
  - 16-byte string: Heartbeat text.
- **Request:**
  - Message type: `0`
  - Text: `"hello"` (UTF-8 encoded, padded or truncated to 16 bytes)
- **Response:**
  - Message type: `0`
  - Text: `"helo world"` (UTF-8 encoded, padded or truncated to 16 bytes)
- **Total Message Size:** 5 bytes (header) + size of payload

### Operation Request

- **Purpose:** Send an arithmetic operation to the server.
- **Payload Format:** `!iBii`
  - 4-byte integer: Message type (`1` for operation request).
  - 1-byte unsigned integer: Operator code
    - `1`: Addition
    - `2`: Subtraction
    - `3`: Multiplication
    - `4`: Division
  - 4-byte integer: First operand
  - 4-byte integer: Second operand
- **Total Message Size:** 5 bytes (header) + size of payload

### Operation Response

- **Purpose:** Return the result of the arithmetic operation.
- **Payload Format:** `!iq`
  - 4-byte integer: Message type (`1` for operation response).
  - 8-byte long integer: Operation result
- **Total Message Size:** 5 bytes (header) + size of payload

## Code Structure

- **calc_protocol.py:**  
  Contains the `CalcProtocol` class with methods to pack and unpack messages. Each method adds or validates the metadata header before processing the payload.

- **network_utils.py:**  
  Provides a utility function to receive a specified number of bytes from a socket, ensuring complete message reads.

- **calc_server.py:**  
  Implements the server. The server:

  - Listens for client connections on a specified host and port.
  - Validates the heartbeat message using the metadata header.
  - Processes the arithmetic operation request.
  - Sends the operation result as a 64-bit integer with the metadata header.

- **calc_client.py:**  
  Implements the client. The client:
  - Connects to the server.
  - Sends a heartbeat message and waits for a valid response.
  - Prompts the user for an arithmetic operation and two integers.
  - Sends the operation request and displays the result received from the server.

## Requirements

- Python 3.x
- Uses only Python's Standard Library

## Running the Project

1. **Start the server:**  
   Open a terminal and run:

   ```bash
   python calc_server.py
   ```

2. **Start the client:**  
   Open a separate terminal and run:

   ```bash
   python calc_client.py
   ```

3. **Use the calculator:**  
   Follow the on-screen prompts in the client terminal to enter the operator code and two integers. The client displays the result returned by the server.

## Error Handling

- The client and server use a utility function to ensure complete reception of fixed-size messages.
- The metadata header is checked to confirm the protocol identifier and version.
- If the heartbeat message or metadata is not valid, the connection is closed.
- Division by zero is handled by returning a result of 0.

## License

This project is provided for demonstration purposes.

## Contact

Refer to the source code files for detailed comments and documentation.
