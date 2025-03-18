import os
import platform
import threading

# Function to extract base IP (e.g., "192.168.153" from "192.168.153.100")
def get_base_ip(ip):
    return ".".join(ip.split(".")[:3])  # Extract first three octets

# Function to ping an IP address
def ping_ip(ip):
    param = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    command = f"ping {param} -w 500 {ip} > nul 2>&1" if platform.system().lower() == "windows" else f"ping {param} -W 1 {ip} > /dev/null 2>&1"

    response = os.system(command)
    if response == 0:
        print(f"[+] Device found: {ip}")

# Function to scan the entire network
def scan_network(base_ip):
    threads = []
    for i in range(1, 255):  # Scanning 192.168.153.1 to 192.168.153.254
        ip = f"{base_ip}.{i}"
        thread = threading.Thread(target=ping_ip, args=(ip,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

# Main function
if __name__ == "__main__":
    user_ip = input("Enter your IP address (e.g., 192.168.153.100): ").strip()
    
    if user_ip.count('.') != 3:
        print("Invalid IP address format!")
    else:
        base_ip = get_base_ip(user_ip)
        print(f"Scanning network {base_ip}.x ...")
        scan_network(base_ip)
        print("Scan complete.")
      
