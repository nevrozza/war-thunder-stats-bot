from threading import Thread
from selenium import webdriver
from bs4 import BeautifulSoup
import psycopg2
from discord_webhook import DiscordEmbed, DiscordWebhook
import myfuncks as fu
import requests
import schedule
import time
import os


db_uri = os.environ.get('DATABASE_URL')


sort_of_players = {}
sorted_players = {}








def time_checker():

    fu.func_parsing_of_players_ts()
    print(str(str(int(time.strftime('%H', time.gmtime())) * 60 + (int(time.strftime('%M', time.gmtime()))))+ str('+'+time.strftime('%S', time.gmtime()))))
    if str(str(int(time.strftime('%H', time.gmtime())) * 60 + (int(time.strftime('%M', time.gmtime()))))+ str('+'+time.strftime('%S', time.gmtime()))) in ['80+00', '110+00', '140+00', '170+00', '200+00', '230+00', '260+00', '290+00', '320+00', '350+00', '380+00', '410+00', '860+00', '890+00', '920+00', '950+00', '980+00', '1010+00', '1040+00', '1070+00', '1100+00', '1130+00', '1160+00', '1190+00', '1220+00', '1250+00', '1280+00']:
        fu.func_parsing_of_squadrons_ts_in_period()
    elif str(str(int(time.strftime('%H', time.gmtime())) * 60 + (int(time.strftime('%M', time.gmtime()))))+ str('+'+time.strftime('%S', time.gmtime()))) in ['50+00',  '830+00']:
        fu.func_parsing_of_squadrons_ts_start()
    elif str(str(int(time.strftime('%H', time.gmtime())) * 60 + (int(time.strftime('%M', time.gmtime()))))+ str('+'+time.strftime('%S', time.gmtime()))) in ['440+00', '1340+00']:
        fu.func_parsing_of_squadrons_ts_last()    
schedule.every(30).seconds.do(time_checker) 
while True:
    
    if time.strftime('%H:%M:%S', time.gmtime()) == os.environ.get('time_start'):
        while True:
    
            schedule.run_pending()
            time.sleep(1) 