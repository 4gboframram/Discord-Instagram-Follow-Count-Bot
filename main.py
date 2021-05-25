import discord
import os
from replit import db
from discord.ext import commands
import random
import asyncio
from glob import glob
import shutil

from keep_alive import keep_alive
from Insta import Instagram
bot = commands.Bot(command_prefix=".",help_command=None)
monitors_is_looping=False

@bot.event
async def on_ready():
	print(f'{bot.user.name} has connected to Discord!')
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="insta follower counts"))
	print('starting monitor update')
	await update_monitors()


@bot.command()
@commands.has_permissions(manage_guild=True)
async def monitor(ctx, media, username, channel_type, name):
	channel=None
	if name.find('[count]')==-1: 
		await ctx.send("You need to use '[count]' in the name of the channel to specify where to put the counter number")
		return

	if channel_type=='text':
		try:
			channel=await ctx.guild.create_text_channel(name.replace(r'[count]', 'NaN'))
		except: 
			await ctx.channel.send("Either I do not have permissions to create the channel, or you did something wrong.")
			return
		try:
			await channel.set_permissions(ctx.guild.default_role, send_messages=False)
		except: await ctx.send('I do not have the permissions to lock the text channel. Deleting channel.')
		
	elif channel_type=='voice':
		try:
			channel=await ctx.guild.create_voice_channel(name.replace(r'[count]', 'NaN'))
		except: 
			await ctx.channel.send("Either I do not have permissions to create the channel, or you did something wrong.")
			
		try:
			await channel.set_permissions(ctx.guild.default_role, connect=False)
		except: 
			await ctx.send('I do not have the permissions to lock the voice channel. Deleting channel.')
			await channel.delete()
			return
	if media=="insta" or media=="instagram":
		media="instagram"
		follower_count=-1
		print(channel.id)
		try:
			
			follower_count=await Instagram(username).async_follow_count()
		except: 
			await ctx.channel.send('Something went wrong with getting your Instagram follower count. Deleting monitor')
			await channel.delete()
			return
		try:
			await channel.edit(name=name.replace(r'[count]', str(follower_count)))
			
		except: 
			await ctx.send("Something went wrong editing the channel name. Deleting channel")
			await channel.delete()
			return

		
	else: await ctx.send(f"'{media}' is not a supported social at the moment")

	db[str(channel.id)]= [name, media, username]
	print(db.keys())
	await ctx.send("Success initializing monitor")

async def update_monitors():
	global monitors_is_looping
	if not monitors_is_looping:
		monitors_is_looping=True
		while True: 
			print("updating monitors...")
			requests=[]
			
			for channel_id in db.keys():
				media_type=db[channel_id][1]
				user=db[channel_id][2]
				
				if media_type=='insta' or media_type=='instagram':
					requests.append(Instagram(user).async_follow_count())
			requests=tuple(requests)
			results=asyncio.gather(*requests)
			values=dict(zip(db.keys(), await results))

			for channel_id in db.keys():
				channel_name=db[channel_id][0]
				channel=bot.get_channel(int(channel_id))
				try:
					await channel.edit(name=channel_name.replace(r'[count]', str(values[channel_id])))
				except AttributeError: del db[channel_id]
			print("Successfully updated monitors")
			await asyncio.sleep(600)

@bot.command()
async def recent(ctx, username, counter=0):
	
	print(f"getting recent for {username}")
	if not os.path.exists(f"{username}"):
		likes, comments=Instagram(username).get_recent_post()
	
	
	media=glob(f'{username}/*mp4')
	media.extend(glob(f'{username}/*jpg'))
	filename=media[counter]
	desc_file=open(glob(f"{username}/*.txt")[0])
	desc=desc_file.read()
	desc_file.close()
	embed=discord.Embed(description=f'({counter+1} of {len(media)})', author=f'Recent post from {username}', color=random.randint(0,2**16-1))
	try: embed.set_footer(text=f'❤{likes}\t💬{comments}')
	except UnboundLocalError: embed.set_footer(text=f'❤UwU\t💬OwO')
	embed.add_field(name=f'{username}', value=f"{desc}", inline=True)
	
	embed.set_image(url=f"attachment://{os.path.basename(filename)}")

	post=await ctx.send(embed=embed, file=discord.File(filename))
	if len(media)>1:
		if counter<0: counter=0
		if counter==0: await post.add_reaction('➡️')
		elif counter==len(media)-1: await post.add_reaction('⬅️')
		else: 
			await post.add_reaction('⬅️')
			await post.add_reaction('➡️')

		
		
		def check(reaction, user):
			emoji=str(reaction.emoji)
			return reaction.message.id==post.id and (emoji=='⬅️' or emoji=='➡️') and not user.bot
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
			print(f'got reaction {str(reaction.emoji)}')
			
			if str(reaction.emoji)=='➡️':
				counter+=1
				await post.delete()
				try: await recent(ctx, username, counter,)
				except:
					counter-=1
					await recent(ctx,username, counter)
				await recent(ctx, username, counter)
			if str(reaction.emoji)=='⬅️':
				counter-=1
				await post.delete()
				try: await recent(ctx, username, counter,)
				except:
					counter+=1
					await recent(ctx,username, counter)
				
		except asyncio.TimeoutError: print(f'removing {username} directory')
	try:
		shutil.rmtree(username)
		return
	except: pass

@bot.command()
async def top(ctx, username, counter=0):
		
	print(f"getting top for {username}")
	if not os.path.exists(f"{username}"):
		likes, comments=Instagram(username).get_top_post()
	
	
	media=glob(f'{username}/*mp4')
	media.extend(glob(f'{username}/*jpg'))
	filename=media[counter]
	desc_file=open(glob(f"{username}/*.txt")[0])
	desc=desc_file.read()
	desc_file.close()
	embed=discord.Embed(description=f'({counter+1} of {len(media)})', author=f'Top post from {username}', color=random.randint(0,2**16-1))
	try: embed.set_footer(text=f'❤{likes}\t💬{comments}')
	except UnboundLocalError: embed.set_footer(text=f'❤UwU\t💬OwO')
	embed.add_field(name=f'{username}', value=f"{desc}", inline=True)
	
	embed.set_image(url=f"attachment://{os.path.basename(filename)}")

	post=await ctx.send(embed=embed, file=discord.File(filename))
	if len(media)>1:
		if counter<0: counter=0
		if counter==0: await post.add_reaction('➡️')
		elif counter==len(media)-1: await post.add_reaction('⬅️')
		else: 
			await post.add_reaction('⬅️')
			await post.add_reaction('➡️')

		
		
		def check(reaction, user):
			emoji=str(reaction.emoji)
			return reaction.message.id==post.id and (emoji=='⬅️' or emoji=='➡️') and not user.bot
		try:
			reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
			print(f'got reaction {str(reaction.emoji)}')
			
			if str(reaction.emoji)=='➡️':
				counter+=1
				await post.delete()
				try: await top(ctx, username, counter,)
				except:
					counter-=1
					await top(ctx,username, counter)
				await top(ctx, username, counter)
			if str(reaction.emoji)=='⬅️':
				counter-=1
				await post.delete()
				try: await top(ctx, username, counter,)
				except:
					counter+=1
					await top(ctx,username, counter)
				
		except asyncio.TimeoutError: 
			print(f'removing {username} directory')
			return
	try:
		shutil.rmtree(username)
		return
	except: return


				
keep_alive() #you should comment this out if you are hosting locally
client=discord.Client()
bot.run(os.getenv('TOKEN'))