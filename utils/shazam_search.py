import requests
import asyncio
from shazamio import Shazam

async def search(dirname, file_name):
  shazam = Shazam()
  
  path = dirname+"/"+file_name
  res = await shazam.recognize_song(path)
  
  if not res['matches']:
  	return (False, "not_found")

  url = res['track']['sections'][2]['youtubeurl']
  url = requests.get(url, timeout=50).json()
  link = url['actions'][0]['uri']
  
  file_name = res['track']['share']['subject']
  return (True, link, file_name)