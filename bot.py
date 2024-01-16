import discord
from discord.ext import commands
from urllib.request import Request, urlopen
import numpy as np
import cv2
import detect_score

def run_discord_bot(token):
    
    intents = discord.Intents.default()
    intents.message_content = True
    # client = discord.Client(intents=intents)
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} is running!')

    @bot.command()
    async def score(ctx):
        username = ctx.author
        channel = ctx.channel
        print(f"{username} called command 'score' in channel: {str(channel)}")
        try:
            async for m in channel.history(limit=2):
                msg = m
            
            url = str(msg.attachments[0].url)
            req = urlopen(Request(url, headers={'User-Agent':'Modzilla/5.0'}))
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            img = cv2.imdecode(arr, -1)

            score,_ = detect_score.score_from_image(img)
            if score != "None" and score <= 6:
                response = f"uhhh i think you scored a {score} on this wordle."
            else:
                response = "that doesn't seem to be wordle..."
        except Exception as e:
            print(e)
            response = "that doesn't seem to be wordle..."
        await ctx.send(response)

    bot.run(token)