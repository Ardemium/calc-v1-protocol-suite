# Client-Server Calculator Protocol

## Overview

This project implements a client-server calculator that uses a custom binary protocol over TCP sockets in Python. The client sends two 32-bit integers and an operator code to the server. The server performs the arithmetic operation and returns the result as a 64-bit integer. A heartbeat message verifies that the server is available before the operation request. Each message includes a fixed metadata header.

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
