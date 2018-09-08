import os
import sys
import json
import spotipy
import spotipy.util as util
from json.decoder import JSONDecodeError

# Get the username from terminal
username = sys.argv[1]
# Define nessisary scope
scope = 'user-read-private user-library-read playlist-modify-public' 

#erase cache and prompt for user permission
try:
	token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
	os.remove(f".cache-{username}")
	token = util.prompt_for_user_token(username, scope)


#create spotify object
spotifyObject = spotipy.Spotify(auth=token)

#get the current user
user = spotifyObject.current_user()
displayName = user['display_name']

startingOffset = 0

playlist_name = input("What would you like the playlist to be called? ")

#create a playlist for the user
spotifyObject.user_playlist_create(username, playlist_name, public=True)

#get the id of the playlist
playlist_id = None
playlists = spotifyObject.current_user_playlists(limit=10)['items']
for item in playlists:
	if item['name'] == playlist_name:
		playlist_id = item['id']
		break

#if the playlist can not be found 
if playlist_id == None:
	raise Exception('Error: playlist can not be found!')



# loop to iterate through saved tracks (nessisary as limit of tracks to pull at once is 50)
while True:
	savedTracks = spotifyObject.current_user_saved_tracks(limit=50, offset=startingOffset)
	tracks = []
	#if there are no new tracks to import
	if savedTracks['items'] == []:
		break
	for item in savedTracks['items']:
		track = item['track']
		tracks.append("spotify:track:" + track['id'])
	startingOffset+=50
	spotifyObject.user_playlist_add_tracks(username, playlist_id, tracks)

print("created playlist "+playlist_name+" and added tracks successfully!")
