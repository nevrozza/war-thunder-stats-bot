import wtrsdb
import discord
BOT_TOKEN = 'OTk2NDAxNTIyNDE2MDM3OTI4.Gk5Pcb.ciVrNhMjWj8hAe0xySRZ7MB22WA9kY9Hw63pVk'
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
                print(message.author.roles)
                wtrsdb.func_parsing_of_top_players_ts()
                return
            if message.content.lower() == '!topsq':
                await message.delete()
                await message.channel.send(f'{message.author.mention} wait for top 20 squadrons in <#997040874141782046>')
                wtrsdb.func_parsing_of_squadrons_ts_in_period()
                return
        if message.content.lower() == '!check':
            await message.delete()
            await message.channel.send(f'{message.author.mention}: {message.author.roles}')
client.run(BOT_TOKEN)