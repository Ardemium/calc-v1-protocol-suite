# **CALC v1 Protocol Wireshark Plugin - FAQ**

### **1. What is the CALC v1 Wireshark Plugin?**

The CALC v1 Wireshark plugin is a custom Lua dissector for analyzing network traffic that uses the CALC v1 binary protocol. When installed, Wireshark will automatically recognize and decode CALC v1 messages instead of displaying raw TCP data.

---

### **2. How do I install the CALC v1 dissector in Wireshark?**

#### **Step-by-Step Installation:**

1. **Find the Wireshark Plugins Folder:**

   - **Windows:**  
     Copy `calc_dissector.lua` to:

     ```plaintext
     %APPDATA%\Wireshark\plugins\
     ```

     You can paste this path into File Explorer and hit Enter to open the folder.

   - **macOS:**  
     Copy `calc_dissector.lua` to:

     ```plaintext
     ~/Library/Application Support/Wireshark/Plugins/
     ```

   - **Linux:**  
     Copy `calc_dissector.lua` to:
     ```plaintext
     ~/.local/lib/wireshark/plugins/
     ```

2. **Restart Wireshark:**  
   This step ensures the new plugin is loaded.

3. **Verify the Plugin is Loaded:**
   - Open Wireshark.
   - Go to **Help > About Wireshark > Plugins**.
   - Look for `calc_dissector.lua` in the list.

---

### **3. How do I test if the CALC v1 protocol is recognized?**

- Start capturing on the relevant network interface.
- Generate CALC v1 traffic by running the `calc_server.py` and `calc_client.py` applications.
- Apply the display filter in Wireshark:

```plaintext
calc
```

- Check if packets are labeled as "CALC" in the **Protocol** column.

---

### **4. What if the protocol is not displayed correctly?**

- **Verify Port Registration:**  
  The dissector is set to recognize CALC protocol traffic on TCP port `6000` by default. Ensure your server and client are communicating on this port.
- **Check the Plugin Path:**  
  Make sure the `calc_dissector.lua` file is in the correct Wireshark plugins directory.
- **Enable Lua Support:**  
  In Wireshark, go to **Edit > Preferences > Protocols > Lua** and ensure that Lua plugins are enabled.
- **View Wireshark Logs:**  
  Any errors in loading the Lua script will appear in Wireshark's **Help > About Wireshark > Internals > Lua Console**.

---

### **5. How can I change the TCP port used by the dissector?**

- **Edit `calc_dissector.lua`:**  
  Change the port number in the following line:

```lua
tcp_port:add(6000, calc_proto)
```

- **Set the new port:**  
  Replace `6000` with your desired TCP port.
- **Restart Wireshark** to apply the changes.

---

### **6. How do I uninstall the CALC v1 plugin?**

- Navigate to the Wireshark plugins directory.
- Delete the `calc_dissector.lua` file.
- Restart Wireshark.

---

### **7. Where can I find more information?**

- Refer to the **RFC.md** file in the repository for a detailed protocol specification.
- The **README.md** file contains setup instructions for the server and client applications.

---

If you need additional help or encounter issues, check the Wireshark logs and ensure your Lua script is error-free.
