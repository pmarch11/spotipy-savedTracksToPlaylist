<h1> Spotipy saved tracks to playlist </h1>

a simple python/spotipy script used to create a playlist out of all songs saved on spotify

<h3> Usage: </h3>

Download the tracksToPlaylist.py to any location on your computer

Set environment variables for CLIENT_ID and SECRET_ID retrieved from: https://developer.spotify.com/dashboard/login
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='http://google.com/'
```
Run the script using 
```
python tracksToPlaylist.py [YOUR_SPOTIFY_URI]
```

Enter a name for the playlist when prompted, wait a minute or so, and voila! the playlist should be showing up in your spotify account