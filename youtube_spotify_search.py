import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests
import re


#ToDo: Fix URls for songs with multiple artists/features
#scrapes lyrics from genius.com
def scrape_lyrics(artist_name, song_name):
        
        #clean up artist and song name
        artist_name_2 = str(artist_name.replace(' ','-')) if ' ' in artist_name else str(artist_name)
        song_name_2 = str(song_name.replace(' ','-')) if ' ' in song_name else str(song_name)
       
       
        #creates html parser
        page = requests.get('https://genius.com/'+artist_name_2 + '-'+ song_name_2 + '-' + 'lyrics')
        html = BeautifulSoup(page.text,'html.parser')

        #collects lyrics from html
        print('https://genius.com/'+artist_name_2 + '-'+ song_name_2 + '-' + 'lyrics')
        lyrics1 = html.find_all("div",attrs={'class':re.compile(r'ReferentFragmentDesktop|Lyrics__Container')})
        lyrics2 = html.find_all("span",attrs={'class':re.compile(r'ReferentFragmentdesktop|Lyrics__Container')})        
        lyrics = []

        #cleans lyric data and loads lyrics into lyrics[]
        if lyrics1:
                 for L in lyrics1:
                        lyrics.append(L.get_text("<br>").replace("<br>", " "))
        elif lyrics2:
                for L in lyrics2:

                        lyrics.append(L.get_text("<br>").replace("<br>", " "))
        else:
                lyrics = None      
        return lyrics

# You need to insert your own client id and secret id fromt he spotify dev menu
#create a spotify app at https://developer.spotify.com/ , click on the drop down menu at the top right and click on dashboard
#this menu will allow you to create an app and gain access to your unique client id and secret_id

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="INSERT CLIENT_ID HERE",
                                               client_secret="INSERT CLIENT_SECRET_ID HERE",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-read-recently-played"))

results = sp.current_user_recently_played(limit=50)

# prints out tracks and lyrics from your spotify most recently played which is capped at 50
#using this for debugging
# currently a bug with the wrong url being generated for songs with multiple artists
for idx, item in enumerate(results['items']):
    track = item['track']
    print(scrape_lyrics( track['artists'][0]['name'], track['name']))
    print(idx, track['artists'][0]['name'], " – ", track['name'])
    for artist in track['artists']:
           print (artist)



search_string = input("Enter in String to search: ")

lyrics = scrape_lyrics("Frank Ocean", "Nights")



for lyric in lyrics:
       if search_string.lower() in lyric.lower():
               print (lyric)

print(search_string)