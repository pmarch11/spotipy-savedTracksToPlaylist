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

print("0 - Create a new playlist")
print("1 - Modify an existing one")
decide = input("Choose 0 or 1: ")


while True:
	if decide == "0":
		playlist_name = input("What would you like the playlist to be called? ")

		spotifyObject.user_playlist_create(username, playlist_name, public=True)
		break

	elif decide == "1":
		playlist_name = input("What is the playlists name? ")
		break
	else:
		print("invalid input")

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

counter = 0



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
	if counter == 0 and decide == "1":
		spotifyObject.user_playlist_replace_tracks(username, playlist_id, tracks)
		counter = 1
	else:
		spotifyObject.user_playlist_add_tracks(username, playlist_id, tracks)

if decide == "0":
	print("created playlist "+playlist_name+" and added tracks successfully!")
elif decide == "1":
	print("modified playlist "+playlist_name+" and added tracks successfully!")
