# UDP NAT Hole-Punching (P2P Chat)

Peer-to-peer chat in Python using UDP NAT hole-punching. Two clients behind NAT connect directly to each other with the help of a rendezvous server.

## How it works

Both clients are behind NAT, their routers block unsolicited incoming traffic. A public rendezvous server exchanges their addresses, then each client sends UDP packets to the other to "punch a hole" in their respective NAT before communicating directly.
The rendezvous server acts as a simplified STUN server (RFC 5389) 
exchanging peer addresses to enable direct P2P communication.

```
Client A  -->  Server  <--  Client B
Client A  <exchanges addresses>  Client B
Client A  <------  direct UDP  ------>  Client B
```

## Why this matters

NAT hole-punching is the technique behind WebRTC, online gaming, and most P2P protocols; any time two peers need to communicate directly without a relay server in the middle.

## Requirements

- Python 3.x
- A public rendezvous server (AWS EC2 or any machine with a public IP)
- Port `12000 UDP` open in the Security Group / firewall

## Usage

**Rendezvous server:**
```bash
python3 server.py
```

**Client A and Client B** - replace `<YOUR_SERVER_IP>` in `client.py` with the server's public IP, then run on each machine:
```bash
python3 client.py
```

## Example
```
Registered to server, waiting for peer...
Peer address: ('203.0.113.42', 54321)
Starting hole punching...
Punch attempt 1
Connection established with ('203.0.113.42', 54321)
Ready to chat!
you: hello
peer: hey!
```

## Known Limitations

### Symmetric NAT

Works with most home routers, but fails with **symmetric NAT**.
With a typical router, your machine always uses the same public port regardless of destination while with symmetric NAT, the router assigns a different public port per destination:
```
your machine : 5000  -->  server  -->  public IP : 54321
your machine : 5000  -->  peer    -->  public IP : 54567  (different!)
```

The peer receives the port used to reach the server, not the one the router will assign for peer traffic. Hole-punching fails. The standard solution is a **TURN relay server** (RFC 5766), which WebRTC falls back to in this case.

### Terminal UI

Since receiving and sending run on separate threads, incoming messages may 
print over the input prompt. This is a display-only issue, messages are 
delivered correctly. A proper fix would require a terminal UI library 
like `prompt_toolkit`.