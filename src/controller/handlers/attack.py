class AttackCommands:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def register(self):
        @self.bot.message_handler(commands=['scan'])
        def scan(message):
            try:
                parts = message.text.split()
                if len(parts) != 3:
                    self.bot.reply_to(message, "Format: /scan device_id target")
                    return
                device_id = parts[1]
                target = parts[2]
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                self.bot.reply_to(message, f"Perintah scan dikirim ke {device_id}\nTarget: {target}")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
