import os
try: from instaloader import Instaloader, Profile
except ImportError: 
	os.system("pip install instaloader") #replit likes to uninstall things
	from instaloader import Instaloader
import pickle
import json
L = Instaloader()

try: L.load_session_from_file(os.getenv('USERNAME'), 'sess.pkl')
except: L.interactive_login(os.getenv('USERNAME'))
L.save_session_to_file(filename="sess.pkl")

L.close()
sess_pickle=open('sess.pkl', 'rb')
sess=pickle.load(sess_pickle)
f=open("cookies.json", 'w+')
json.dump(sess, f)
sess_pickle.close()
f.close()