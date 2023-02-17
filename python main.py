# Import function to support operability
import os
from background import keep_alive

import telebot
import openai
import requests

# Authenticate with OpenAI
openai.api_key = "OPOENAI_API"

# Authenticate with Telegram 2x times
bot = telebot.TeleBot("YOUR_TELEGRAM_TOKEN")
os.environ["TELEGRAM_TOKEN"] = "YOUR_TELEGRAM_TOKEN"

# Define a function to handle text messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text(message):
    # Show typing indication
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Generate a prompt based on user's message
    prompt = f"Пожалуйста, напишите продолжение для следующего параграфа:\n{message.text}\n\nПродолжение:"

    # Call the OpenAI API to generate text based on the prompt
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        bot.reply_to(message, "Извините, произошла ошибка при обработке вашего запроса.")
        return

    # Extract the text from the OpenAI API response
    continuation = response.choices[0].text

    # Split the continuation into multiple messages if it exceeds the Telegram message length limit
    for i in range(0, len(continuation), 4096):
        # Send the message with typing indication
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, continuation[i:i+4096])

# Define a function to handle photo messages
@bot.message_handler(func=lambda message: True, content_types=['photo'])
def handle_photo(message):
    # Show typing indication
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Get the file ID of the photo
    file_id = message.photo[-1].file_id

    # Call the Telegram API to get the file path of the photo
    file_path = bot.get_file(file_id).file_path

    # Download the photo from Telegram's servers
    photo_url = f"https://api.telegram.org/file/bot{os.environ['TELEGRAM_TOKEN']}/{file_path}"
    photo_data = requests.get(photo_url).content

    # Call the OpenAI API to generate a caption for the photo
    try:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Пожалуйста, дайте подпись к этой фотографии:\n{photo_url}\n\nПодпись:",
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    except Exception as e:
        bot.reply_to(message, "Извините, произошла ошибка при обработке вашего запроса.")
        return

    # Extract the caption from the OpenAI API response
    caption = response.choices[0].text

    # Split the caption into multiple messages if it exceeds the Telegram message length limit
    for i in range(0, len(caption), 4096):
        # Send the message with typing indication
        bot.send_chat_action(message.chat.id, 'typing')
        bot.reply_to(message, caption[i:i+4096])

# Start the flask server in a separate thread in background
keep_alive()

# Start the bot polling loop
bot.polling(non_stop=True, interval=0) 
