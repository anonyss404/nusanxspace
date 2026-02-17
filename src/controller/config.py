import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))
    
    def validate(self):
        if not self.BOT_TOKEN:
            print("❌ ERROR: BOT_TOKEN ga ada di .env!")
            print("📝 Edit file .env dan isi token lo")
            exit(1)
        if self.ADMIN_ID == 0:
            print("❌ ERROR: ADMIN_ID ga ada di .env!")
            print("📝 Edit file .env dan isi ID lo")
            exit(1)
        print("✅ Config berhasil dimuat")
