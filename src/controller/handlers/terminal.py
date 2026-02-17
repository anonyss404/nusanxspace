class TerminalCommands:
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
    
    def register(self):
        @self.bot.message_handler(commands=['lock_terminal'])
        def lock_terminal(message):
            try:
                parts = message.text.split(',')
                if len(parts) != 3:
                    self.bot.reply_to(message, "Format: /lock_terminal,device_id,password")
                    return
                cmd, device_id, password = parts
                device_id = device_id.strip()
                password = password.strip()
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                self.db.update_terminal(device_id, is_locked=1)
                self.bot.reply_to(message, f"Terminal {device_id} terkunci! 🔒")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
        
        @self.bot.message_handler(commands=['unlock_terminal'])
        def unlock_terminal(message):
            try:
                parts = message.text.split()
                if len(parts) != 2:
                    self.bot.reply_to(message, "Format: /unlock_terminal device_id")
                    return
                device_id = parts[1]
                terminal = self.db.get_terminal(device_id)
                if not terminal:
                    self.bot.reply_to(message, f"Terminal {device_id} nggak ditemukan!")
                    return
                self.db.update_terminal(device_id, is_locked=0)
                self.bot.reply_to(message, f"Terminal {device_id} terbuka! 🔓")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
        
        @self.bot.message_handler(commands=['delete_terminal'])
        def delete_terminal(message):
            try:
                parts = message.text.split()
                if len(parts) != 2:
                    self.bot.reply_to(message, "Format: /delete_terminal device_id")
                    return
                device_id = parts[1]
                self.db.delete_terminal(device_id)
                self.bot.reply_to(message, f"Terminal {device_id} dihapus! 💀")
            except Exception as e:
                self.bot.reply_to(message, f"Error: {str(e)}")
