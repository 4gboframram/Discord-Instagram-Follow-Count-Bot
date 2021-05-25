# Usage:
Assuming you know how to create your own discord bot
## Replit:
- 1: Clone this repo
- 2: Set `USERNAME` secret for when you run from `main.py`. `USERNAME` should be your Instagram username (you should probably use an alt so you don't get your main banned). Also set `TOKEN` to be your bot's token
- 3: Go to the shell and run `python`
- 4: Run `import os; os.environ['USERNAME']='{username}'; os.system('python get_cookies.py')`, where {username} is your Instagram username. 
We have to do this because the 'secrets' (environment variables) we set in part 2 only work for `main.py`
- 5: Enter your Instagram password when prompted
- 6: You should see the `cookies.json` and `sess.pkl` file. Copy the contents, go to secrets and create the secret named 'INSTACOOKIES' with a value of the contents `cookies.json`
- 7: Delete `cookies.json` and `sess.pkl`
- 8: You should just be able to run

## Other: 
wip
## Commands

`.monitor [media], [username], [channel type], [name]`: creates a channel with a name that monitors a (instagram) user's follower count. For now, the `[media]` argument only accepts 'insta' or 'instagram'. `[Channel type]` should either 'voice' or 'text'. The `[name]` must contain "[count]" so the bot knows where to put the counter, and should be surrounded by quotes. 

`.top [username]`: sends the media and description of the most recent post from the user. If there are multiple slides, you can scroll through them.
`.top [username]`: sends the media and description of the most top post from the user. If there are multiple slides, you can scroll through them. For this bot, the top post is determined with `likes+3*comments`. 
