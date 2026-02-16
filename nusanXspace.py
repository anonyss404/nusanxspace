import os
import sys
import time
import signal
import socket
import threading
from dotenv import load_dotenv

from utils.banner import BANNER
from utils.helpers import fake_scan_progress, check_lock
from modules.subdomain_scanner import SubdomainScanner
from modules.dir_bruteforce import DirBruteforce
from modules.port_scanner import PortScanner
from modules.sql_injection import SQLInjection
from modules.xss_finder import XSSFinder
from core.telegram_bot import TelegramBot

load_dotenv()

def signal_handler(sig, frame):
    if check_lock():
        print("\n[!] Terminal terkunci! Tidak bisa keluar!")
        print("[!] Minta admin buka dulu...")
        return
    else:
        print("\n\n[•] Exiting NUSANXSPACE...")
        bot.send_message(f"👋 Terminal {DEVICE_ID} dimatikan")
        sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def get_device_id():
    try:
        return socket.gethostname() + "_" + str(os.getpid())
    except:
        return "unknown_device"

DEVICE_ID = get_device_id()
bot = TelegramBot(DEVICE_ID)

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

def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print(BANNER)
    
    bot_thread = threading.Thread(target=bot.start, daemon=True)
    bot_thread.start()
    
    print("[✓] Connected to Telegram Controller")
    print("[✓] Device ID: " + DEVICE_ID)
    print("[!] All scans are for educational purposes only\n")
    time.sleep(2)
    
    while True:
        if check_lock() or bot.locked:
            os.system('clear' if os.name == 'posix' else 'cls')
            print(BANNER)
            print("\n" + "="*50)
            print("🔒 TERMINAL TERKUNCI! 🔒".center(50))
            print("="*50)
            print("\nTerminal ini dikunci oleh admin!")
            print("Tidak bisa menggunakan tools sampai dibuka!")
            print("\nTekan CTRL+C untuk mencoba keluar...")
            time.sleep(5)
            continue
        
        os.system('clear' if os.name == 'posix' else 'cls')
        print(BANNER)
        target = input(MENU).strip()
        
        if not target:
            continue
        
        choice = input("\nPilih menu (1-9): ").strip()
        
        scanners = {
            '1': SubdomainScanner(),
            '2': DirBruteforce(),
            '3': PortScanner(),
            '4': SQLInjection(),
            '5': XSSFinder()
        }
        
        if choice in scanners:
            bot.send_message(f"📡 Terminal {DEVICE_ID} menjalankan {scanners[choice].name} on {target}")
            scanners[choice].run(target)
            fake_scan_progress()
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
            print("\nHasil akan ditampilkan di layar")
            input("\nTekan Enter untuk kembali...")
        
        elif choice == '9':
            print("\n[•] Exiting NUSANXSPACE...")
            bot.send_message(f"👋 Terminal {DEVICE_ID} dimatikan")
            time.sleep(1)
            sys.exit(0)
        
        else:
            print("\n[!] Pilihan tidak valid!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        if check_lock() or bot.locked:
            print("\n\n[!] TERMINAL TERKUNCI!")
            print("[!] Tidak bisa keluar paksa!")
            print("[!] Minta admin buka dulu...")
            while True:
                time.sleep(10)
        else:
            print("\n\n[•] Exiting...")
            bot.send_message(f"👋 Terminal {DEVICE_ID} dimatikan")
            sys.exit(0)
