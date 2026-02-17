import sqlite3
import os
import json
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='terminals.db'):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.c = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS terminals
                         (id INTEGER PRIMARY KEY AUTOINCREMENT,
                          device_id TEXT UNIQUE,
                          device_name TEXT,
                          phone_model TEXT,
                          android_version TEXT,
                          battery_level INTEGER,
                          ip_address TEXT,
                          location TEXT,
                          last_seen TIMESTAMP,
                          is_locked BOOLEAN DEFAULT 0,
                          lock_password TEXT)''')
        self.conn.commit()
    
    def register_terminal(self, device_id, device_info):
        self.c.execute('''INSERT OR REPLACE INTO terminals 
                         (device_id, device_name, phone_model, android_version, 
                          battery_level, ip_address, location, last_seen, is_locked)
                         VALUES (?,?,?,?,?,?,?,?,?)''',
                      (device_id, 
                       device_info.get('device_name', 'Unknown'),
                       device_info.get('phone_model', 'Unknown'),
                       device_info.get('android_version', 'Unknown'),
                       device_info.get('battery_level', 0),
                       device_info.get('ip_address', '0.0.0.0'),
                       json.dumps(device_info.get('location', {})),
                       datetime.now(),
                       0))
        self.conn.commit()
    
    def update_terminal(self, device_id, **kwargs):
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            values.append(value)
        values.append(device_id)
        query = f"UPDATE terminals SET {', '.join(fields)} WHERE device_id = ?"
        self.c.execute(query, values)
        self.conn.commit()
    
    def get_terminal(self, device_id):
        self.c.execute("SELECT * FROM terminals WHERE device_id = ?", (device_id,))
        return self.c.fetchone()
    
    def get_all_terminals(self):
        self.c.execute("SELECT device_id, device_name, last_seen, is_locked FROM terminals")
        return self.c.fetchall()
    
    def delete_terminal(self, device_id):
        self.c.execute("DELETE FROM terminals WHERE device_id = ?", (device_id,))
        self.conn.commit()
