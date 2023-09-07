import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
import re
from termcolor import colored
from selenium import webdriver
import logging
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from lyricsgenius import Genius 




def scrape_youtube_history(email,password):
       logger = logging.getLogger('selenium')

       logger.setLevel(logging.DEBUG)
       driver = uc.Chrome()
       driver.get('https://accounts.google.com/')
       driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(email)
       driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
       time.sleep(15)
       driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
       driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
       time.sleep(15)


       
       #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


       page_source = driver.get('https://www.youtube.com/feed/history')

       #html = BeautifulSoup(page_source,'html')

       #history = html.find_all('a',attrs={'id':'thumbnail'})

       #link_history = []

       #for event in history:
        #      link_history.append(event['href'])
        
       #print (link_history)
       return []




if __name__ == '__main__':

        #enter your credentials here
        spotify_client_id = "ENTER SPOTIFY CLIENT ID HERE"
        spotify_secret_id = "ENTER SPOTIFY SECRET ID HERE"

        youtube_email = "ENTER YOUTUBE EMAIL HERE"
        youtube_password = "ENTER YOUTUBE PASSWORD HERE"

        genius = Genius("ENTER YOUR GENIUS.COM ACCESS TOKEN HERE")

#You need to install the genius python api from https://lyricsgenius.readthedocs.io/en/master/setup.html, easy to isntall with pip install lyricsgenius
#Then you need to create a genius.com access token from here https://docs.genius.com/




# You need to insert your own client id and secret id fromt he spotify dev menu
#create a spotify app at https://developer.spotify.com/ , click on the drop down menu at the top right and click on dashboard
#this menu will allow you to create an app and gain access to your unique client id and secret_id

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                 client_secret=spotify_secret_id,
                                                redirect_uri="http://localhost:8888/callback",
                                                 scope="user-read-recently-played"))



        results = sp.current_user_recently_played(limit=50)

# prints out tracks and lyrics from your spotify most recently played which is capped at 50
#using this for debugging
# currently a bug with the wrong url being generated for songs with multiple artists
        """for idx, item in enumerate(results['items']):
        track = item['track']
        print(scrape_lyrics( track['artists'][0]['name'], track['name']))
        print(idx, track['artists'][0]['name'], " – ", track['name'])
        for artist in track['artists']:
                 print (artist)"""


        #scrape youtube history and return cc data
        #youtube_history = scrape_youtube_history(youtube_email,youtube_password)
       
       
        search_string = input("Enter in String to search: ")
        search_string = search_string.lower()

#TO DO:
#finds if the search_string matches the lyrics 
#prints out the match with the search_string highlighted in red
        for idx, item in enumerate(results['items']):
                track = item['track']
                artist = track['artists'][0]['name']
                song= track['name']
                song1 = genius.search_song(song, artist)
                if song1 is not None:      
                        lyrics = song1.lyrics
                        if len(lyrics)>0:
                                lyric = lyrics.lower()
                                if search_string in lyric:
                                        print ("\033[1m"+artist + ": " + song +"\033[0m"+"-" + lyric.replace(search_string,colored(search_string,'red')))
                                        print("\n\n\n\n")

