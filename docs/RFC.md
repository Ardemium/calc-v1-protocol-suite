# **CALC v1 Protocol Specification**

### **Document Version:** 1.0

### **Last Updated:** 08/03/2025

### **Author:** Ardemium

---

## **1. Introduction**

The CALC v1 protocol is a custom binary protocol designed for a simple client-server calculator application over TCP. The protocol facilitates arithmetic operations between a client and a server using a fixed-format binary message structure.

This document outlines the protocol's message structure, valid field values, and expected behaviors according to the CALC v1 specification.

---

## **2. Protocol Overview**

The CALC v1 protocol operates over TCP, using a fixed 5-byte metadata header followed by a specific message payload.

### **2.1 Metadata Header**

| Field       | Size | Type           | Description                     |
| ----------- | ---- | -------------- | ------------------------------- |
| Magic Bytes | 4    | String (ASCII) | Constant value `"CALC"`.        |
| Version     | 1    | Unsigned Byte  | Protocol version, fixed to `1`. |

### **2.2 Supported Message Types**

| Message Type | Value | Description                                      |
| ------------ | ----- | ------------------------------------------------ |
| `HEARTBEAT`  | `0`   | Used for server liveness checks.                 |
| `REQUEST`    | `1`   | Request for performing an arithmetic operation.  |
| `RESPONSE`   | `1`   | Server response containing the operation result. |

---

## **3. Message Formats**

### **3.1 Heartbeat Message**

#### **Request Format**

| Field        | Size | Type           | Value     | Description                      |
| ------------ | ---- | -------------- | --------- | -------------------------------- |
| Message Type | 4    | Signed Integer | `0`       | Indicates a heartbeat message.   |
| Text         | 16   | String (ASCII) | `"hello"` | Padded or truncated to 16 bytes. |

#### **Response Format**

| Field        | Size | Type           | Value          | Description                      |
| ------------ | ---- | -------------- | -------------- | -------------------------------- |
| Message Type | 4    | Signed Integer | `0`            | Indicates a heartbeat response.  |
| Text         | 16   | String (ASCII) | `"helo world"` | Padded or truncated to 16 bytes. |

##### **Example**

```
CALC v1 Protocol Data
    Magic Bytes: CALC
    Version: 1
    Message Type: 0
    Text: hello
```

```
CALC v1 Protocol Data
    Magic Bytes: CALC
    Version: 1
    Message Type: 0
    Text: helo world
```

---

### **3.2 Operation Request Message**

#### **Request Format**

| Field         | Size | Type           | Description                           |
| ------------- | ---- | -------------- | ------------------------------------- |
| Message Type  | 4    | Signed Integer | `1`, indicating an operation request. |
| Operator Code | 1    | Unsigned Byte  | Specifies the arithmetic operation.   |
| Number 1      | 4    | Signed Integer | First operand.                        |
| Number 2      | 4    | Signed Integer | Second operand.                       |

##### **Operator Codes**

| Code | Operation      | Description                                        |
| ---- | -------------- | -------------------------------------------------- |
| `1`  | Addition       | Returns `Number 1 + Number 2`.                     |
| `2`  | Subtraction    | Returns `Number 1 - Number 2`.                     |
| `3`  | Multiplication | Returns `Number 1 * Number 2`.                     |
| `4`  | Division       | Returns `Number 1 // Number 2` (integer division). |

##### **Example**

```
CALC v1 Protocol Data
    Magic Bytes: CALC
    Version: 1
    Message Type: 1
    Operator Code: 4
    Number 1: 64
    Number 2: 16
```

---

### **3.3 Operation Response Message**

#### **Response Format**

| Field        | Size | Type           | Description                            |
| ------------ | ---- | -------------- | -------------------------------------- |
| Message Type | 4    | Signed Integer | `1`, indicating an operation response. |
| Result       | 8    | Signed Long    | The result of the operation.           |

##### **Example**

```
CALC v1 Protocol Data
    Magic Bytes: CALC
    Version: 1
    Message Type: 1
    Result: 4
```

---

## **4. Message Flow**

### **4.1 Heartbeat Check**

1. **Client** sends a `HEARTBEAT` request (`"hello"`).
2. **Server** responds with `"helo world"`.
3. If the response is invalid, the client closes the connection.

### **4.2 Operation Request/Response**

1. **Client** sends an `OPERATION REQUEST` message with operator code and operands.
2. **Server** performs the operation:
   - If division by zero is requested, the server returns `0` as the result.
3. **Server** sends an `OPERATION RESPONSE` message with the result.

---

## **5. Error Handling**

| Scenario                             | Handling                  |
| ------------------------------------ | ------------------------- |
| Invalid Magic Bytes or Version       | Drop connection.          |
| Unrecognized Message Type            | Ignore and log error.     |
| Division by Zero (`Operator Code 4`) | Return `0` as the result. |
| Incomplete Message                   | Drop connection.          |

---

## **6. Security Considerations**

- The CALC v1 protocol does not include authentication or encryption.
- It is recommended to run the protocol over a secure transport layer (e.g., TLS).
- Input validation is performed on all message types to avoid malformed requests.

---

## **7. Example Byte Streams**

### **7.1 Heartbeat Request (Hex)**

```
43 41 4C 43 01 00 00 00 00 68 65 6C 6C 6F 00
00 00 00 00 00 00 00 00 00 00 00 00 00
```

### **7.2 Heartbeat Response (Hex)**

```
43 41 4C 43 01 00 00 00 00 68 65 6C 6F 20 77
6F 72 6C 64 00 00 00 00 00 00 00 00 00
```

### **7.3 Operation Request (Division)**

```
43 41 4C 43 01 00 00 00 01 04 00 00 00 40 00
00 00 10
```

### **7.4 Operation Response (Result: 4)**

```
43 41 4C 43 01 00 00 00 01 00 00 00 00 00 00
00 04
```

---

## **8. Future Versions and Extensions**

- Future protocol versions may introduce additional operation types or enhanced metadata.
- Extended metadata may support operation chaining, error codes, and detailed diagnostics.

---

## **9. Conclusion**

The CALC v1 protocol provides a simple, well-defined method for arithmetic operation requests over TCP. This specification serves as a foundation for extending the protocol with more complex operations and enhanced security features in future versions.
