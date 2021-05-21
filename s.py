import re
import json
from time import sleep, perf_counter
import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

options = Options()
options.headless = True
INSTACOOKIES=json.loads(os.environ['INSTACOOKIES'])
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
class Instagram:
	def __init__(self, browser):
		self.browser = browser
		print("Redirecting to Instagram...")
		self.browser.get(f"https://www.instagram.com/")

	def login(self, username, password):
		print("Logging in...")
		print("Inputting username...")
		username_input = self.browser.find_element_by_css_selector("input[name='username']")
		print("Inputting password...")
		password_input = self.browser.find_element_by_css_selector("input[name='password']")
		username_input.send_keys(username)
		password_input.send_keys(password)
		login_button = self.browser.find_element_by_xpath("//button[@type='submit']")
		print("Logging in...")
		login_button.click()

		sleep(5)
		return self
	def goto_user_page(self, user):
		print("Redirecting to the user page...")
		return InstaUserPage(self.browser, user)
	def save_cookies(self):
		cookies_file=open('cookies.json', 'w+')
		json.dump(self.browser.get_cookies(), cookies_file)
		cookies_file.close()

class InstaUserPage(Instagram):
	def __init__(self, browser, user):
		self.browser=browser
		self.browser.get("https://www.instagram.com/")
		for cookie in INSTACOOKIES:
			self.browser.add_cookie(cookie)
		self.browser.get(f"https://www.instagram.com/{user}")
		self.response=self.browser.page_source
	def get_follower_count(self):
		followers=re.search(r'edge_followed_by":{"count":\d+}', self.response)
		follower_count=followers.group(0).replace('edge_followed_by":{"count":', '').replace('}', '')
		print(follower_count)
		return int(follower_count)
timer1=perf_counter()
print("Opening web browser")
browser = webdriver.Firefox(options=options)

user_page=InstaUserPage(browser, "myon.gardener")
user_page.get_follower_count()
user_page.save_cookies()
timer2=perf_counter()
browser.close()
print(f"Took {timer2-timer1} seconds to get follower count")
