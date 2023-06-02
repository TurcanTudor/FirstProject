import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_uri = "http://localhost:8000/callback"

scope = "playlist-modify-public playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Open and read the html file where I saved all my songs 
with open('all_songs.html','r') as file:
    html_code = file.read()

soup = BeautifulSoup(html_code, 'html.parser')

p_tags = soup.find_all('p', class_='p1')
# Create a new Playlist
playlist_name = 'All my Music'
playlist_description = 'Containts all my music'
playlist = sp.user_playlist_create(user='YOUR_USERNAME',name=playlist_name,public=True,description=playlist_description)

track_uris = []
if p_tags:
    for p_tag in p_tags:
        # Extract the desired text
        artist = p_tag.contents[4]
        song = p_tag.contents[0]
        #print(f'Song: {song}  Artist: {artist}')

        #Search for the track on Spotify
        query = f"{song} {artist}"
        results = sp.search(q=query,type='track',limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
            print(f"Added track '{song}' by '{artist} to the playlist '{playlist_name}'")
        else:
            print(f" NO TRACK found for '{song} by '{artist} on Spotify")

else:
    print("No <p> tags with class 'p1' found.")

#add all the tracks to the playlist
batch_size =100
for i in range(0,len(track_uris),batch_size):
    batch_tracks = track_uris[i:i+batch_size]
    sp.playlist_add_items(playlist_id=playlist['id'],items=batch_tracks)
print("All Tracks added to the Playlist Succesfully")
