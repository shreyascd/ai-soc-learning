# Day 3 – Reflection: How a Web Request Travels (OSI Layers)

1. **Application** – Browser builds an HTTP request (e.g. GET /page) when you type a URL.
2. **Transport** – TCP breaks it into segments and sets up a connection with the server (three-way handshake).
3. **Network** – IP adds source/destination addresses so the packet can be routed across networks.
4. **Data Link** – Frames are built with MAC addresses to move the packet across the local network/router hops.
5. **Physical** – Bits travel as electrical/optical/radio signals through cables or Wi-Fi to reach the server, which processes the request and sends the response back through the same layers in reverse.
