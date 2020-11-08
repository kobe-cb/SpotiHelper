import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
import json
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#SET
#CLIENT_ID = ''
#CLIENT_SECRET = ''
#redirect_uri = 'http://google.com/'

#Get the username from terminal(passed in thru terminal)
username = sys.argv[1]
scope ='user-read-private user-read-playback-state user-modify-playback-state'

#User ID: qtixhb2op20rjv4fpm8k2a540

#Erase cache and prompt for user permisisn (Thru spot website)

try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#Create our spotify object
spotifyObject = spotipy.Spotify(auth=token)

user = spotifyObject.current_user()

#Get current device
devices = spotifyObject.devices()
deviceID = devices['devices'][0]['id']

#Current Track information
track = spotifyObject.current_user_playing_track()
artist = track['item']['artists'][0]['name']
track = track['item']['name']

displayName = user['display_name']
followers = user['followers']['total']

while True:
    print()
    print(">>> Welcome to Spotipy! <<<")
    print(">> Logged in as: " + displayName + " <<")
    if artist != "":
        print("> Currently playing " + artist + " - " + track +" <")

    print()
    print("1 - Play a song by an Artist")
    print("2 - Randomize a playlist's order")
    print("3 - Your Stats (:")
    print("4 - exit\n")
    choice = input("Your choice: ")

    #Search for the artist
    if choice == "1":
        print()
        searchQuery = input("Please enter the Artist's Name: ")
        print()

        #get search results
        searchResults = spotifyObject.search(searchQuery, 1, 0, "artist")

        #artist details
        artist = searchResults['artists']['items'][0]
        print(artist['name'])
        print(str(artist['followers']['total']) + " followers")
        print(artist['genres'][0])
        print()
        webbrowser.open(artist['images'][0]['url'])
        artistID = artist['id']

        #Album and track details
        trackURIS = []
        trackArt = []
        z = 0

        #Extract album data
        albumResults = spotifyObject.artist_albums(artistID)
        albumResults = albumResults['items']

        for item in albumResults:
            print("ALBUM " + item['name'])
            albumID = item['id']
            albumArt = item['images'][0]['url']

            #Extract track data
            trackResults = spotifyObject.album_tracks(albumID)
            trackResults = trackResults['items']

            for item in trackResults:
                print(str(z) + ": " + item['name'])
                trackURIS.append(item['uri'])
                trackArt.append(albumArt)
                z += 1
            print()


        #See the album art
        while True:
            print("======================================================================")
            songSelection = input("Enter a song number to see the album art and play the song(x to exit): ")
            if songSelection == "x":
                break
            trackSelectionList = []
            trackSelectionList.append(trackURIS[int(songSelection)])
            spotifyObject.start_playback(deviceID, None, trackSelectionList)
            webbrowser.open(trackArt[int(songSelection)])


    #Randomizer
    if choice == "2":
        #api calls that we're gonna use:
        #current_user_playlists
        #goal: allow the user to choose a target playlist, populate the playlist's song URIs into an array
        #populate the array into a target playlist (the user is supposed to create a new one)
        #randomize the ordering of the songs
        break


    if choice == "3":
        print("====================================================")
        print(">> You have " + str(followers) + " followers")
        print()
        followed_Artists = spotifyObject.current_user_playlists(3)
        print("Your top three playlists are: ")
        playlist_Names = followed_Artists['items'][0]['name']
        print("- Playlist 1: " + playlist_Names)
        playlist_Names = followed_Artists['items'][1]['name']
        print("- Playlist 2: " + playlist_Names)
        playlist_Names = followed_Artists['items'][2]['name']
        print("- Playlist 3: " + playlist_Names)
        #print()
        print("====================================================")



    #Exit program
    if choice == "4":
        break
#PRINTS JSON IN READABLE FORMAT
# print(json.dumps(VARIABLE, sort_keys=True, indent=4))