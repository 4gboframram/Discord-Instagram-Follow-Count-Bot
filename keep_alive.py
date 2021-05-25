#This file is used to keep the replit active
#If you're using replit, you can use this.
#To use, use uptimerobot to ping the 
#site replit creates every at least 20 minutes

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is online"

def run():
  app.run(host='0.0.0.0' ,port=8000)

def keep_alive():  
    t = Thread(target=run)
    t.start()

