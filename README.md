# 📡 Raspberry Pi Auto IP Sender 🚀  
Automatically detects and sends **WiFi, Ethernet, and Public IP** to a Telegram bot whenever the Raspberry Pi starts or network changes.

## 🎯 Features  
✅ Auto-runs on boot using **systemd**  
✅ Detects **WiFi & Ethernet IPs**  
✅ Fetches **Public IP**  
✅ Sends updates to **Telegram Bot**  
✅ Runs in the background & updates only when IP changes  

---

## 🔧 Installation  

### 1️⃣ Install Required Packages  
```bash
sudo apt update && sudo apt install python3 python3-pip -y
pip3 install requests
```

### 2️⃣ Create a Telegram Bot  
1. Open Telegram and search for **BotFather**  
2. Send `/newbot` and follow instructions  
3. Get your **BOT_TOKEN** from BotFather  
4. Get your **CHAT_ID** using [this guide](https://stackoverflow.com/a/32572159)  

---

## 📜 Setup the Python Script  

### 3️⃣ Clone This Repository  
```bash
git clone https://github.com/yourusername/raspberry-pi-ip-bot.git
cd raspberry-pi-ip-bot
```

### 4️⃣ Create & Edit Configuration  
```bash
nano config.py
```
Paste this and update your **BOT_TOKEN** and **CHAT_ID**:
```python
BOT_TOKEN = "your_telegram_bot_token"
CHAT_ID = "your_telegram_chat_id"
```

### 5️⃣ Create the Script  
```bash
nano auto_ip_sender.py
```
Paste this:
```python
import requests
import time
import socket
import subprocess

from config import BOT_TOKEN, CHAT_ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

def get_ip():
    try:
        wifi_ip = subprocess.getoutput("hostname -I | awk '{print $1}'")
        eth_ip = subprocess.getoutput("ip -4 addr show eth0 | grep inet | awk '{print $2}' | cut -d'/' -f1")
        public_ip = requests.get("https://api64.ipify.org").text
        return wifi_ip, eth_ip, public_ip
    except Exception as e:
        return None, None, None

def send_ip():
    wifi_ip, eth_ip, public_ip = get_ip()
    if wifi_ip or eth_ip:
        message = f"🚀 *Raspberry Pi Started!*\n🔷 *WiFi IP:* `{wifi_ip}`\n🔷 *Ethernet IP:* `{eth_ip}`\n🌍 *Public IP:* `{public_ip}`"
        requests.post(TELEGRAM_API_URL, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"})

prev_ips = None

while True:
    current_ips = get_ip()
    if current_ips != prev_ips:
        send_ip()
        prev_ips = current_ips
    time.sleep(30)  # Check every 30 seconds
```
Save and exit: `CTRL + X`, `Y`, `Enter`

---

## ⚙️ Setup Auto Start with systemd  

### 6️⃣ Create a Systemd Service  
```bash
sudo nano /etc/systemd/system/ip_monitor.service
```
Paste this:
```ini
[Unit]
Description=Auto IP Sender for Raspberry Pi
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/raspberry-pi-ip-bot/auto_ip_sender.py
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
Save and exit: `CTRL + X`, `Y`, `Enter`

### 7️⃣ Enable & Start the Service  
```bash
sudo systemctl daemon-reload
sudo systemctl enable ip_monitor.service
sudo systemctl start ip_monitor.service
```

---

## 🔍 Checking Logs & Debugging  

📌 **Check Service Status**  
```bash
sudo systemctl status ip_monitor.service
```

📌 **View Logs**  
```bash
journalctl -u ip_monitor.service --no-pager --reverse | head -50
```

📌 **Restart the Service**  
```bash
sudo systemctl restart ip_monitor.service
```

📌 **Stop the Service**  
```bash
sudo systemctl stop ip_monitor.service
```

---

## 🎯 Done! Now, your Raspberry Pi will:  
✅ Send **IP updates** to your Telegram bot on **boot & IP change**  
✅ Run in the **background**  
✅ Auto-restart if it crashes  

💡 If you found this useful, **star this repo ⭐** and share it! 🚀  

