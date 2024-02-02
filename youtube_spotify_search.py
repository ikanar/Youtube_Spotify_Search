import spotipy
from spotipy.oauth2 import SpotifyOAuth
from termcolor import colored
import undetected_chromedriver as uc
import time
from selenium.webdriver.common.by import By
from lyricsgenius import Genius
from selenium.webdriver.common.keys import Keys 
from pytube import extract
from youtube_transcript_api import YouTubeTranscriptApi
import datetime



#logs a user into their google account
#navigates to the youtube.com/feed/history 
#scrapes the links from the thumbnails
#cleans up links
#returns list of links
def scrape_youtube_history(email,password):

       driver = uc.Chrome()
       driver.get('https://accounts.google.com/')
       driver.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(email)
       driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button/span').click()
       time.sleep(15)
       driver.find_element(By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input').send_keys(password)
       driver.find_element(By.XPATH, '//*[@id="passwordNext"]/div/button/span').click()
       time.sleep(15)



       driver.get('https://www.youtube.com/feed/history')



       scan_length = 5

       while scan_length > 0:
            elem = driver.find_element(By.TAG_NAME, "html")
            elem.send_keys(Keys.END)
            time.sleep(4)
            scan_length = scan_length - 1
       elements = driver.find_elements(By.XPATH,'//*[@id="video-title"]')    
        

      
       history = {}

    #loads links from html elements into a list 
    #filters out the "None" elements
       for element in elements:
               title = element.get_attribute("title")
               e = element.get_attribute("href")
               if e != None:
                       id = extract.video_id(e)
                       history[title] = id

       return history

def get_youtube_cc_data (youtube_history):
       
       cc_data = {}

       for event in youtube_history:
               transcript = YouTubeTranscriptApi.get_transcript(youtube_history[event])
               cc_data[event] = transcript
       return cc_data

def main():
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
        #scrape youtube history and return cc data
        youtube_history = scrape_youtube_history(youtube_email,youtube_password)

        youtube_cc_data = get_youtube_cc_data(youtube_history)
       
       
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

#prints out the match with the youtube_cc_data
        for video_title in youtube_cc_data:
                for line in youtube_cc_data[video_title]:
                        if search_string in line['text']:
                                print(video_title)
                                print(line['text'].replace(search_string,colored(search_string,'red')))
                                convert = str(datetime.timedelta(seconds = line['start']))
                                print("Time: " + convert)
                                print("\n\n\n")         

if __name__ == '__main__':

        main()