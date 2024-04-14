import os
import urllib
import music_tag
import spotipy
from spotipy import SpotifyOAuth
from dotenv import load_dotenv

path = "Diric"
files = os.listdir(path)

for file_name in files:
    if file_name[:2] == "._" or file_name == ".DS_Store":
        continue

    audio_file = path + "/" + file_name
    audio_mt = music_tag.load_file(audio_file)

    if audio_mt['artist'] == "":
        continue

    query = f"{str(audio_mt['title'])} {str(audio_mt['artist']).replace(',', ' ')}"
    dotenv_path = './.env'

    load_dotenv(dotenv_path)
    SpClient = os.getenv('SP_CLIENT_ID')
    SpSecret = os.getenv('SP_CLIENT_SECRET')

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SpClient,
                                                     client_secret=SpSecret,
                                                     redirect_uri='http://localhost:7777/callback'))

    search_results = sp.search(query, type="track")
    track = search_results['tracks']['items'][0]

    track_id = track['id']
    track_title = track['name']
    track_artists = [artist['name'] for artist in track['artists']]
    album_id = track['album']['id']
    album_search = sp.album(album_id)
    album_title = album_search['name']
    album_artists = [artist['name'] for artist in album_search['artists']]
    year = album_search['release_date'][0:4]
    disc_no = track['disc_number']
    pos = track['track_number']
    cover_url = album_search['images'][0]['url']

    urllib.request.urlretrieve(cover_url, "image.jpg")
    with open('image.jpg', 'rb') as img_file:
        audio_mt['artwork'] = img_file.read()

    audio_mt['tracktitle'] = track_title
    audio_mt['artist'] = ', '.join(track_artists)
    audio_mt['album'] = album_title
    audio_mt['albumartist'] = ', '.join(album_artists)
    audio_mt['tracknumber'] = pos
    audio_mt['discnumber'] = disc_no
    audio_mt['year'] = year
    audio_mt.save()
