import os
import re
import json
import requests
import aiohttp
import asyncio
import time
from itertools import islice
import pickle
try: from instaloader import Instaloader, Profile
except ImportError: 
	os.system("pip install instaloader")
	from instaloader import Instaloader, Profile

if not __name__=='__main__':
	global INSTACOOKIES
	INSTACOOKIES=json.loads(os.environ['INSTACOOKIES'])
	global USERNAME
	USERNAME=os.environ['USERNAME']
	global PASSWORD
	PASSWORD=os.environ['PASSWORD']

s={INSTACOOKIES[3]['name']: INSTACOOKIES[3]['value'], INSTACOOKIES[7]['name']: INSTACOOKIES[7]['value']}
serialized = pickle.dumps(s)
with open('sess.pkl','wb') as file_object:
    file_object.write(serialized)

L = Instaloader()
L.load_session_from_file(USERNAME,'sess.pkl')
os.remove('sess.pkl')
class Instagram:
	
	def __init__(self, user):
		self.user=user
		self.response=None
		self.recent_post=None
		self.profile=Profile.from_username(L.context, self.user)
	def get_follow_count(self):
		s = requests.Session()
		for cookie in INSTACOOKIES:
			s.cookies.set(cookie['name'], cookie['value'])
		self.response = s.get(f"https://www.instagram.com/{self.user}").text
		reg=re.compile(r'edge_followed_by":{"count":(\d+)}')
		follower_str=reg.search(self.response)
		follow_count=follower_str.group(1)
		print(follow_count)
		return int(follow_count)
	async def async_follow_count(self):
		cookies={INSTACOOKIES[3]['name']: INSTACOOKIES[3]['value']}
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
	Instagram("myon.gardener").get_recent_post()
	"""loop = asyncio.get_event_loop()
	loop.run_until_complete()"""


		



