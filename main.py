import bot
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    token = os.getenv("TOKEN")
    bot.run_discord_bot(token)