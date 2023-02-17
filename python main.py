# Import function to support operability
import os
from background import keep_alive

import telebot
import openai
import time

bot = telebot.TeleBot("YOUR_BOT_TOKEN")
openai.api_key = "OPENAI_API"

# Initialize the conversation state dictionary
conversations = {}

@bot.message_handler(content_types=["text"])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text

    # Check if the chat_id already has a conversation state saved
    if chat_id in conversations:
        # If it does, append the new message to the conversation context
        context = conversations[chat_id]['context'] + ' ' + text
        # Save the updated conversation context
        conversations[chat_id]['context'] = context
    else:
        # If it doesn't, create a new conversation state and context
        context = text
        conversations[chat_id] = {'context': context}

    # Show typing indication
    bot.send_chat_action(chat_id, 'typing')

    # Generate the response using the OpenAI API
    response = openai.Completion.create(
        engine="davinci", 
        prompt=context, 
        max_tokens=512, 
        n=1, 
        stop=None, 
        temperature=0.5
    ).choices[0].text

    # Split the response into multiple messages if it is too long
    max_message_length = 2048
    num_messages = int(len(response) / max_message_length) + 1
    for i in range(num_messages):
        start = i * max_message_length
        end = (i + 1) * max_message_length
        message_text = response[start:end]
        bot.send_message(chat_id, message_text)

    # Update the conversation context with the response
    conversations[chat_id]['context'] = context + ' ' + response

# Start the flask server in a separate thread in background
keep_alive()

# Start the bot polling loop
bot.polling(non_stop=True, interval=0) 
