import os
import sys
import time
import random

def fake_scan_progress():
    tools = [
        "Subdomain Scanner", "Directory Bruteforce", 
        "Port Scanner", "SQL Injection Tester", "XSS Finder"
    ]
    tool = random.choice(tools)
    print(f"\n[•] Initializing {tool}...")
    for i in range(0, 101, 20):
        print(f"\r[•] Progress: {i}%", end="")
        time.sleep(0.5)
    print(f"\n[✓] {tool} completed!")
    print("[•] Analyzing results...")
    time.sleep(1)
    print("[✓] Analysis complete!")
    print("\n[!] No vulnerabilities found!")
    print("[!] Target seems secure!\n")

def check_lock():
    lock_file = "/data/local/tmp/.nusan_lock"
    if os.path.exists(lock_file):
        with open(lock_file, 'r') as f:
            status = f.read().strip()
        return status == "LOCKED"
    return False
