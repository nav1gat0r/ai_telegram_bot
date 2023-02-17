# Import function to support operability
import os
from background import keep_alive #импорт функции для поддержки работоспособности

import telebot
import openai

bot = telebot.TeleBot("YOUR_BOT_TOKEN")
openai.api_key = "OPENAI_API"

# initialize context dictionary to store conversation context
context = {}

@bot.message_handler(content_types=["text"])
def handle_text(message):
    # get the article name from the message
    article_name = message.text
    
    # check if the article name is already in the context dictionary
    if article_name in context:
        # if it is, use the existing context
        prompt = context[article_name]
    else:
        # if it isn't, create a new context with just the article name
        prompt = f"{article_name}: "
    
    # add the user's message to the prompt and get response from GPT
    prompt += message.text
    response = openai.Completion.create(
        engine="code-davinci-002",
        prompt=prompt,
        max_tokens=8000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    bot.send_message(message.chat.id, response.choices[0].text)
    
    # update the context dictionary with the new context
    context[article_name] = prompt

# Start the flask server in a separate thread.
keep_alive()

# Start the bot
bot.polling(non_stop=True, interval=0) 
