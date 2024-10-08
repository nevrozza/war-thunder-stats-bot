from discord_webhook import DiscordEmbed, DiscordWebhook
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import psycopg2
import os
db_uri = os.environ.get('DATABASE_URL')


sort_of_players = {}
sorted_players = {}

def parsing_of_squadrons(naming):
    if naming == 'start':
        webhook_squadrons = DiscordWebhook(url = os.environ.get('webhook_squadrons_old'))
        ds_squadrons = DiscordEmbed(title = 'Leaderboard of squadrons(Initial)', color = 'ff0000', url = 'https://warthunder.com/en/community/clansleaderboard')
    elif naming == 'start_new_day':
        webhook_squadrons = DiscordWebhook(url = os.environ.get('webhook_squadrons_old'))
        ds_squadrons = DiscordEmbed(title = 'Leaderboard of squadrons(Initial)', color = 'ff0000', url = 'https://warthunder.com/en/community/clansleaderboard')   
        webhook_new_day = DiscordWebhook(url = os.environ.get('webhook_squadrons_old'))
        ds_new_day = DiscordEmbed(title = '--------------------------------------------------------------------------------------', color = 'ff0000')
        webhook_new_day.add_embed(ds_new_day)
        webhook_new_day.execute(remove_embeds=True) 
    elif naming == 'last':
        webhook_squadrons = DiscordWebhook(url = os.environ.get('webhook_squadrons_old'))
        ds_squadrons = DiscordEmbed(title = 'Leaderboard of squadrons(Ending)', color = 'ff0000', url = 'https://warthunder.com/en/community/clansleaderboard')    
    elif naming == 'norm':
        webhook_squadrons = DiscordWebhook(url = os.environ.get('webhook_squadrons'))
        ds_squadrons = DiscordEmbed(title = 'Leaderboard of squadrons', color = 'ff0000', url = 'https://warthunder.com/en/community/clansleaderboard')
    elif naming == 'norm_new_day':
        webhook_squadrons = DiscordWebhook(url = os.environ.get('webhook_squadrons'))
        ds_squadrons = DiscordEmbed(title = 'Leaderboard of squadrons', color = 'ff0000', url = 'https://warthunder.com/en/community/clansleaderboard')
        webhook_new_day = DiscordWebhook(url = os.environ.get('webhook_squadrons'))
        ds_new_day = DiscordEmbed(title = '--------------------------------------------------------------------------------------', color = 'ff0000')
        webhook_new_day.add_embed(ds_new_day)
        webhook_new_day.execute(remove_embeds=True)
    ds_squadrons.set_timestamp()
    db = psycopg2.connect(db_uri, sslmode = 'require')
    sql = db.cursor()
    top_change = 0
    rank_change = 0
    kills_change = 0
    deaths_change = 0
    kd_change = 0
    count_players_change = 0
    top_int = 0
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path='/app/.chromedriver/bin/chromedriver', options=options)
    driver.get("https://warthunder.com/en/community/clansleaderboard/")
    lnks=driver.find_elements('tag name', "a")
    for lnk in lnks:
        url = lnk.get_attribute('href')
        if url[0:45] == 'https://warthunder.com/en/community/claninfo/':
            top_int += 1
            r = requests.get(url)
            bs = BeautifulSoup(r.text, 'lxml')
            rank_bs = bs.find(class_="squadrons-counter__value")
            air_bs = bs.find("li", class_="squadrons-stat__item-value").find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
            ground_bs = bs.find("li", class_="squadrons-stat__item-value").find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
            deaths_bs = bs.find("li", class_="squadrons-stat__item-value").find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next().find_next()
            name_bs = bs.find(class_="squadrons-info__title")
            count_players_bs = bs.find(class_ = 'squadrons-info__meta-item')
            count_players = int(str(count_players_bs.text).split('Number of players: ')[1].replace(' ', ""))
            name = str((name_bs.text).split('[')[1].split(']')[0]).replace('╌', '').replace('╈', '').replace('╉', '').replace('╏', '').replace('╍', '').replace('_', '').replace('╙', '').replace('═', '').replace('║', '').replace('x', '').replace('╖', '').replace('╎', '').replace('┺', '').replace('┻', '').replace('╝', '').replace('╚', '').replace('╌', '').replace('╊', '').replace('╋', '')
            kills = int(air_bs.text)+int(ground_bs.text)
            rank = int(rank_bs.text)
            deaths = int(deaths_bs.text)
            kd = float('{:.2f}'.format(kills/deaths))
            ###COMPARATION
            try:
                if naming == 'last': sql.execute(f"SELECT rank FROM period_squadrons WHERE name = '{name}'")
                else:    
                    sql.execute(f"SELECT rank FROM squadrons WHERE name = '{name}'")
                top_change = int(top_int)  - sql.fetchone()[0]
                if naming == 'last': sql.execute(f"SELECT points FROM period_squadrons WHERE name = '{name}'")
                else:
                    sql.execute(f"SELECT points FROM squadrons WHERE name = '{name}'")
                rank_change = rank  - sql.fetchone()[0]
                if naming == 'last': sql.execute(f"SELECT kills FROM period_squadrons WHERE name = '{name}'")
                else:
                    sql.execute(f"SELECT kills FROM squadrons WHERE name = '{name}'")
                old_kills = sql.fetchone()[0]
                kills_change = kills  - old_kills
                if naming == 'last': sql.execute(f"SELECT deaths FROM period_squadrons WHERE name = '{name}'")
                else:
                    sql.execute(f"SELECT deaths FROM squadrons WHERE name = '{name}'")
                old_deaths = sql.fetchone()[0]
                deaths_change = deaths  - old_deaths
                kd_change = float('{:.2f}'.format(kd - float('{:.2f}'.format(old_kills/old_deaths))))
                if naming == 'last': sql.execute(f"SELECT players FROM period_squadrons WHERE name = '{name}'")
                else:
                    sql.execute(f"SELECT players FROM squadrons WHERE name = '{name}'")
                count_players_change = count_players - sql.fetchone()[0]           
            except: None
            
            ###NEW
            try:
                if naming == 'start' or naming == 'start_new_day':
                    sql.execute(f"DELETE FROM period_squadrons WHERE name = '{name}'")
                    db.commit()
                else:
                    sql.execute(f"DELETE FROM squadrons WHERE name = '{name}'")
                    db.commit()
                
            except Exception as ex: 
                print(ex)
                sql.execute('ROLLBACK')
                db.commit
            if naming == 'start' or naming == 'start_new_day':
                sql.execute("INSERT INTO period_squadrons(name, rank, points, kills, deaths, players) VALUES(%s, %s, %s, %s, %s, %s)", (name, top_int, rank, kills, deaths, count_players))
                db.commit() 
            else:
                sql.execute("INSERT INTO squadrons(name, rank, points, kills, deaths, players) VALUES(%s, %s, %s, %s, %s, %s)", (name, top_int, rank, kills, deaths, count_players))
                db.commit() 
            
            
            print(f"""
#{top_int}
Name: {name}
Points: {rank}
Kills: {kills}
Deaths: {deaths}
K/D: {kd}
Players: {count_players}
""")
            if top_change == 0:
                a = top_int
            elif top_change > 0:
                a = top_int
                name = f'{name} 🔻(-{top_change})'
            elif top_change < 0:
                a = top_int
                name = f'{name} <:small_green_triangle:996827805725753374>(+{abs(top_change)})'

            if rank_change == 0:
                rank = rank
            elif rank_change > 0:
                rank = f'{rank} <:small_green_triangle:996827805725753374>(+{rank_change})'
            elif rank_change < 0:
                rank = f'{rank} 🔻({rank_change})'
            
            if kills_change == 0:
                kills = kills
            elif kills_change > 0:
                kills = f'{kills} (+{kills_change})'
            elif kills_change < 0:
                kills = f'{kills} ({kills_change})'
            
            if deaths_change == 0:
                deaths = deaths
            elif deaths_change > 0:
                deaths = f'{deaths} (+{deaths_change})'
            elif deaths_change < 0:
                deaths = f'{deaths} ({deaths_change})'
            
            
            if kd_change == 0:
                kd = kd
            elif kd_change > 0:
                kd = f'{kd} <:small_green_triangle:996827805725753374>(+{kd_change})'
            elif kd_change < 0:
                kd = f'{kd} 🔻({kd_change})'
            
            
            if count_players_change == 0:
                count_players = count_players
            elif count_players_change > 0:
                count_players = f'{count_players} <:small_green_triangle:996827805725753374> (+{count_players_change})'
            elif count_players_change < 0:
                count_players = f'{count_players} 🔻({count_players_change})'
            ds_squadrons.add_embed_field(name = f'#{a} {name}', value = f'**Points**: {rank}\n **Kills**: {kills}\n **Deaths**: {deaths} \n **K\D**: {kd} \n **Members**: {count_players}')


            
    driver.close()
    driver.quit()
    webhook_squadrons.add_embed(ds_squadrons)
    webhook_squadrons.execute(remove_embeds=True)
def parsing_of_players(count):
    webhook_channel_players = DiscordWebhook(url = os.environ.get('webhook_channel_players'))
    webhook_top_players = DiscordWebhook(url = os.environ.get('webhook_channel_players'))
    webhook_channel_players_2 = DiscordWebhook(url = os.environ.get('webhook_channel_players'))
    ds_channel_players_2 = DiscordEmbed(title = 'Active players', color = 'ff0000', url = 'https://warthunder.com/en/community/claninfo/Ukrainian%20Atamans')
    ds_channel_players = DiscordEmbed(title = 'Active players', color = 'ff0000', url = 'https://warthunder.com/en/community/claninfo/Ukrainian%20Atamans')
    ds_channel_players.set_timestamp()
    ds_top_players = DiscordEmbed(title = 'TOP 20', color = 'ff0000', url = 'https://warthunder.com/en/community/claninfo/Ukrainian%20Atamans')
    ds_top_players.set_timestamp()
    db = psycopg2.connect(db_uri, sslmode = 'require')
    sql = db.cursor()
    discord_players = 0
    top_player_change = 0
    rank_player_change = 0
    r = requests.get("https://warthunder.com/ru/community/claninfo/Ukrainian%20Atamans")
    bs = BeautifulSoup(r.text, 'lxml')
    count_players_bs = bs.find(class_ = 'squadrons-info__meta-item')
    count_players = int(str(count_players_bs.text).split('Количество игроков: ')[1].replace(' ', ""))
    a_bs = bs.find(class_="squadrons-members__grid-item")
    
    
    a_bs = bs.find(class_="squadrons-members__grid-item")         
    if count == 20:
        for top_int in range(1, 21):
            a_bs = a_bs.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
            name_bs = a_bs.find_next_sibling()
            rank_bs = name_bs.find_next_sibling()
            
            name = str(str(name_bs.text).strip())
            rank = int(str(rank_bs.text).strip())
            a_bs = bs.find(class_="squadrons-members__grid-item")  
            while list(sorted_players.keys())[top_int-1] != name:
                a_bs = a_bs.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
                name_bs = a_bs.find_next_sibling()
                rank_bs = name_bs.find_next_sibling()
                name = str(str(name_bs.text).strip())
                rank = int(str(rank_bs.text).strip())

            try:
                sql.execute(f"SELECT rank FROM top_players WHERE name = '{name}'")
                top_player_change = int(top_int)  - sql.fetchone()[0]
                sql.execute(f"SELECT points FROM top_players WHERE name = '{name}'")
                rank_player_change = rank  - sql.fetchone()[0]
            except: None
                
            try:
                sql.execute(f"DELETE FROM top_players WHERE name = '{name}'")
                db.commit()
                    
            except Exception as ex: 
                print(ex)
                sql.execute('ROLLBACK')
                db.commit 
            sql.execute("INSERT INTO top_players(name, rank, points) VALUES(%s, %s, %s)", (name, top_int, rank))
            db.commit()
            if top_player_change == 0:
                top_int = top_int
            elif top_player_change > 0:
                name = f'{name} 🔻(-{top_player_change})' 
            elif top_player_change < 0:
                name = f'{name} <:small_green_triangle:996827805725753374>(+{abs(top_player_change)})'
            if rank_player_change == 0:
                rank = rank
            elif rank_player_change > 0:
                rank = f'{rank} <:small_green_triangle:996827805725753374>(+{rank_player_change})'
                
            elif rank_player_change < 0:
                rank = f'{rank} 🔻({rank_player_change})'


            ds_top_players.add_embed_field(name = f'#{top_int} {name}', value = f'**Points**: {rank}')
                
            
                
            
            print(f"""
# {top_int}
Name: {name}
Points: {rank}
""")

        
        webhook_top_players.add_embed(ds_top_players)
        webhook_top_players.execute(remove_embeds=True)
        
    if count == 1:
        a_bs = bs.find(class_="squadrons-members__grid-item") 
        for top_int in range(0, count_players):
            a_bs = a_bs.find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling().find_next_sibling()
            name_bs = a_bs.find_next_sibling()
            rank_bs = name_bs.find_next_sibling()
            
            name = str(str(name_bs.text).strip())
            rank = int(str(rank_bs.text).strip())
             
            
                

            try:
                sql.execute(f"SELECT points FROM players WHERE name = '{name}'")
                rank_player_change = rank  - sql.fetchone()[0]
            except: None
                
            try:
                sql.execute(f"DELETE FROM players WHERE name = '{name}'")
                db.commit()
                    
            except Exception as ex: 
                print(ex)
                sql.execute('ROLLBACK')
                db.commit 
            sql.execute("INSERT INTO players(name, points) VALUES(%s,  %s)", (name, rank))
            db.commit()
            if rank_player_change == 0:
                pass
            elif rank_player_change > 0:
                
                discord_players +=1
                if discord_players >= 25:
                    
                    ds_channel_players_2.add_embed_field(name = f'{name}', value = f'**Points**: {rank} <:small_green_triangle:996827805725753374>(+{rank_player_change})')
                else:   
                    
                    ds_channel_players.add_embed_field(name = f'{name}', value = f'**Points**: {rank} <:small_green_triangle:996827805725753374>(+{rank_player_change})')
                
            elif rank_player_change < 0:
                
                discord_players +=1
                if discord_players >= 25:
                    
                    ds_channel_players_2.add_embed_field(name = f'{name}', value = f'**Points**: {rank} 🔻({rank_player_change})')
                else:
                    
                    ds_channel_players.add_embed_field(name = f'{name}', value = f'**Points**: {rank} 🔻({rank_player_change})')
                
            
                
            
           

        if discord_players >= 1:
            webhook_channel_players.add_embed(ds_channel_players)
            webhook_channel_players.execute(remove_embeds=True)
        if discord_players >= 25:
            webhook_channel_players_2.add_embed(ds_channel_players_2)
            webhook_channel_players_2.execute(remove_embeds=True)        


 
def func_parsing_of_top_players_ts():
    parsing_of_top_players_ts = Thread(target=parsing_of_players, args=[20])
    parsing_of_top_players_ts.start()  
def func_parsing_of_players_ts():
    parsing_of_top_players_ts = Thread(target=parsing_of_players, args=[1])
    parsing_of_top_players_ts.start()  
def func_parsing_of_squadrons_ts_last():
    parsing_of_squadrons_ts = Thread(target = parsing_of_squadrons, args = ['last']) 
    parsing_of_squadrons_ts.start()
def func_parsing_of_squadrons_ts_start():
    parsing_of_squadrons_ts = Thread(target = parsing_of_squadrons, args=['start']) 
    parsing_of_squadrons_ts.start()    
def func_parsing_of_squadrons_ts_in_period():
    parsing_of_squadrons_ts = Thread(target = parsing_of_squadrons, args=['norm']) 
    parsing_of_squadrons_ts.start()

def func_parsing_of_squadrons_ts_in_period_new_day():
    parsing_of_squadrons_ts = Thread(target = parsing_of_squadrons, args=['norm_new_day']) 
    parsing_of_squadrons_ts.start()

def func_parsing_of_squadrons_ts_start_new_day():
    parsing_of_squadrons_ts = Thread(target = parsing_of_squadrons, args=['start_new_day']) 
    parsing_of_squadrons_ts.start()