import sys
reload(sys)
sys.setdefaultencoding('utf8')
import time
import spotipy
import spotipy.util as util
import requests
import xmltodict
import re
import json
import htmlentitydefs, re
import codecs

scope='playlist-read-private playlist-modify-private playlist-modify-public'
username=<YOUR_SPOTIFY_USERNAME>
playlist=<TARGET_SPOTIFY_PLAYLIST>
token=''

def renew():
	global token
	token = util.prompt_for_user_token(username,scope,client_id='<CLIENTID>',client_secret='<CLIENTSECRET>',redirect_uri='<CALLBACKURL>')
	return

previous= 'none'
interval  = 150
renew()
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})

if token:
	sp = spotipy.Spotify(auth=token)
	while (1):
		url = 'http://radarlisboa.fm/wp-content/themes/beaton/radio/currentsong.php?url=http://centova.radios.pt:8497'+'&_'+ str(int(time.time())) 
		page = session.get(url)
		rfm = page.text

		rfm = rfm.replace("+","")
		rfm = rfm.replace("&amp;","&")
		rfm = rfm.replace("&apos;","'")
		rfm = rfm.decode('unicode_escape').encode('ascii','ignore')

		if (len(rfm)<1):
			pass
		elif (rfm == previous):
			pass
		else:
			previous=rfm
			search_str = rfm
			try:
				result = sp.search(search_str,type='track',market='PT')
			except spotipy.client.SpotifyException:
				renew()
				sp = spotipy.Spotify(auth=token)
				result = sp.search(search_str,type='track',market='PT')
			if (result['tracks']['items']):
				try:
					sp.user_playlist_remove_all_occurrences_of_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
					sp.user_playlist_add_tracks(username,playlist,[result['tracks']['items'][0]['uri']])
				except:
					print("Exception caught on remove/add ["+rfm+"]")
			else:
				print "Song does not exist: ["+rfm+ "]" 
		time.sleep(interval)
else:
	print "Can't get token for ",username
