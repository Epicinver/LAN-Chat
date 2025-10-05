# chat
import os
import socket
import threading
import datetime

def title(newtitle):
    os.system(f"title {newtitle}")

title("Chat")

PORT = 54545
BROADCAST_IP = "255.255.255.255"

username = input("Enter your name: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # ✅ allow reuse
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("", PORT))

def listen():
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            msg = data.decode(errors="ignore")
            if not msg.startswith(username + ":"):
                print(f"\r{msg}\n> ", end="")
        except Exception as e:
            print(f"Error: {e}")

threading.Thread(target=listen, daemon=True).start()

print(f"🌐 Connected to LAN Chat ({PORT}) — everyone on the network can see messages.")
print("Type 'exitquitplzohio' to quit.\n")

while True:
    msg = input("> ")
    if msg.lower() == "exitquitplzohio":
        print("Goodbye!")
        break
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    full_msg = f"[{timestamp}] {username}: {msg}"
    sock.sendto(full_msg.encode(), (BROADCAST_IP, PORT))
