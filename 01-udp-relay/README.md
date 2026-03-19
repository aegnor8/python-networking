# UDP Socket - Client & Server

Low-level UDP socket implementation in Python. The server receives a message and returns it in uppercase.

## Why UDP

At the transport layer, every internet connection is either **TCP** or **UDP** — HTTP, WebSocket, WebRTC are all built on top of one of these two. This project works directly at that level.

## Why EC2 instead of a local machine?

The problem with running the server locally: both machines are behind NAT, and a router only forwards traffic that was requested from the inside. Deploying on **AWS EC2** provides a public IP with no NAT in the way.

## Requirements

- Python 3.x
- AWS EC2 instance with port `12000 UDP` open in the Security Group

## Usage

**Server (EC2):**
```bash
python3 server.py
```

**Client** — replace `<YOUR_SERVER_IP>` with the EC2 public IP, then:
```bash
python3 client.py
```

## Example

```
input lowercase message: hello world
response: HELLO WORLD
```