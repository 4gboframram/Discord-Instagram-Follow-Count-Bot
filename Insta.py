import os
import re
import json
import requests
import aiohttp
import asyncio
from itertools import islice
import pickle
try: from instaloader import Instaloader, Profile
except ImportError: #replit likes to uninstall things
	os.system("pip install instaloader")
	from instaloader import Instaloader, Profile

if not __name__=='__main__':
	global INSTACOOKIES
	INSTACOOKIES=json.loads(os.getenv('INSTACOOKIES'))
	global USERNAME
	USERNAME=os.getenv('USERNAME')
	global PASSWORD #unused. I originally had it be used before I used Instaloader
	PASSWORD=os.getenv('PASSWORD')

serialized = pickle.dumps(INSTACOOKIES)
with open('sess.pkl','wb') as file_object:
    file_object.write(serialized)

L = Instaloader()
L.load_session_from_file(USERNAME,'sess.pkl')
os.remove('sess.pkl')

#The main Instagram class
class Instagram:
	
	def __init__(self, user):
		self.user=user
		self.response=None
		self.recent_post=None
		self.profile=Profile.from_username(L.context, self.user)

	#original code I had before going async
	def get_follow_count(self):
		s = requests.Session()
		s.cookies.set(INSTACOOKIES['sessionid'])
		self.response = s.get(f"https://www.instagram.com/{self.user}").text
		reg=re.compile(r'edge_followed_by":{"count":(\d+)}')
		follower_str=reg.search(self.response)
		follow_count=follower_str.group(1)
		print(follow_count)
		return int(follow_count)

	async def async_follow_count(self):
		cookies=INSTACOOKIES
		async with aiohttp.ClientSession(cookies=cookies) as s:
			async with s.get(f"https://www.instagram.com/{self.user}") as response:
				
				self.response=await response.text()
				reg=re.compile(r'edge_followed_by":{"count":(\d+)}')
				follower_str=reg.search(self.response)
				follow_count=follower_str.group(1)
				print(follow_count)
				return int(follow_count)

	def get_recent_post(self):
		for post in islice(self.profile.get_posts(), 1):
			L.download_post(post, self.user)
			return (post.likes, post.comments) 
		return (post.likes, post.comments)

	def get_top_post(self):
		
		posts_sorted = sorted(self.profile.get_posts(), key=lambda p: p.likes + 3*p.comments, reverse=True)

		for post in islice(posts_sorted, 1):
			L.download_post(post, self.user)
			return (post.likes, post.comments) 

if __name__=='__main__':
	asyncio.gather(Instagram("myon.gardener").get_recent_post()) #my friend
	


		



