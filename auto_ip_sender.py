import os
import time
import socket
import requests
import subprocess

# 🔹 Telegram Bot Credentials (Replace with your details)
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with your actual bot token
TELEGRAM_CHAT_ID = "Your_Telegram_Chat_ID"  # Your Telegram Chat ID

# 🔹 Store previous IPs to detect changes
previous_local_ips = {}
previous_public_ip = None

# 🔹 Function to check internet connectivity
def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# 🔹 Function to get local IPs (WiFi & Ethernet)
def get_local_ips():
    local_ips = {}
    try:
        interfaces = os.popen("ip -o -4 addr show | awk '{print $2, $4}'").read().strip().split("\n")
        for interface in interfaces:
            iface, ip = interface.split()
            if "eth" in iface:  # Ethernet
                local_ips["Ethernet"] = ip.split("/")[0]
            elif "wlan" in iface:  # WiFi
                local_ips["WiFi"] = ip.split("/")[0]
    except Exception as e:
        print(f"[-] Error getting local IPs: {e}")
    return local_ips

# 🔹 Function to get public IP
def get_public_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=text", timeout=5)
        return response.text.strip()
    except:
        return None  # Return None if unable to get public IP

# 🔹 Function to send IP details to Telegram
def send_ip_to_telegram(local_ips, public_ip):
    message = "🚀 Raspberry Pi Network Update!\n"
    
    for conn, ip in local_ips.items():
        message += f"🔹 {conn} IP: {ip}\n"
    
    if public_ip:
        message += f"🌍 Public IP: {public_ip}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[+] IP update sent to Telegram!")
        else:
            print("[-] Failed to send IP. Check bot token and chat ID.")
    except Exception as e:
        print(f"[-] Error sending Telegram message: {e}")

# 🔹 Main function
def main():
    global previous_local_ips, previous_public_ip

    print("[+] Waiting for internet connection...")
    while not is_connected():
        time.sleep(5)  # Check every 5 seconds

    print("[+] Internet connected! Sending IP details...")

    # Get Local & Public IPs and send first message
    local_ips = get_local_ips()
    public_ip = get_public_ip()
    send_ip_to_telegram(local_ips, public_ip)

    # Store the first IPs
    previous_local_ips = local_ips
    previous_public_ip = public_ip

    print("[+] Now monitoring for IP changes in the background...")

    # Background monitoring
    while True:
        time.sleep(30)  # Check every 30 seconds
        if not is_connected():
            print("[-] Internet lost! Waiting to reconnect...")
            while not is_connected():
                time.sleep(5)  # Wait for internet to return
            print("[+] Internet reconnected!")

        # Check for new IPs
        local_ips = get_local_ips()
        public_ip = get_public_ip()

        # If IP changed, send an update
        if local_ips != previous_local_ips or public_ip != previous_public_ip:
            print("[+] Network change detected! Sending update...")
            send_ip_to_telegram(local_ips, public_ip)
            previous_local_ips = local_ips
            previous_public_ip = public_ip

# 🔹 Run the script
if __name__ == "__main__":
    main()
      
