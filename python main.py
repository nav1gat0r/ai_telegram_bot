# Import function to support operability
from background import keep_alive 

import os
import openai
import telegram
from telegram.ext import Updater, MessageHandler, CommandHandler, filters

# Fetching keys
BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPEN_AI_API")

# Authenticating with OpenAI
openai.api_key = OPENAI_API_KEY

# Defining the message handler function
def message_handler(update, context):
    # Getting the user's message
    message = update.message.text

    # Generating a response from OpenAI's GPT-3
    response = openai.Completion.create(
        engine="davinci",
        prompt=message,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Sending the response back to the user
    update.message.reply_text(response.choices[0].text)

# Creating the bot and registering the message handler function
bot = telegram.Bot(token=BOT_TOKEN)
updater = Updater(token=BOT_TOKEN, use_context=True)
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))

# Starting the bot
updater.start_polling()
updater.idle()


# Start the flask server in a separate thread.
keep_alive()
