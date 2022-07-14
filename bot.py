from threading import Thread
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import psycopg2
from discord_webhook import DiscordEmbed, DiscordWebhook
import myfuncks as fu
import requests
import discord
sort_of_players = {}
sorted_players = {}

db_uri = os.environ.get('DATABASE_URL')
db = psycopg2.connect(db_uri, sslmode = 'require')
sql = db.cursor()
BOT_TOKEN = os.environ.get('BOT_TOKEN')
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
         return
    if message.channel.name == 'управление':
        if "<Role id=997106365413720104 name='123'>" in str(message.author.roles):
            if message.content.lower() == '!top':
                await message.delete()
                await message.channel.send(f'{message.author.mention} wait for top 20 players in <#996836535645241354>')
                fu.func_parsing_of_top_players_ts()
                        
                return
            if message.content.lower() == '!topsq':
                await message.delete()
                await message.channel.send(f'{message.author.mention} wait for top 20 squadrons in <#997040874141782046>')
                fu.func_parsing_of_squadrons_ts_in_period()
                
                return
        if message.content.lower() == '!check':
            await message.delete()
            await message.channel.send(f'{message.author.mention}: {message.author.roles}')
client.run(BOT_TOKEN)