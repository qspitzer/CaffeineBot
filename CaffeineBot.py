import discord
from discord.ext.commands import Bot
from discord.ext import commands
from threading import Thread
import os, sys, traceback
import json
import asyncio
import sqlite3

totalGuilds = 0

def firstConfig():
	token = input("What is the token for your bot user?> ")
	prefix = input("What do you the command prefix to be?(default: $)> ")
	if prefix == None or prefix == '':
		prefix = '$'

	pm = input("Would you like to pm users the help text?(Y/n)> ")
	if pm.lower() != 'n':
		pm = True
	elif pm.lower() == 'n':
		pm = False
	
	defaultChannel = input("What is the name of the default channel for the server?(default: general)> ")
	if defaultChannel == '':
		defaultChannel = 'general'
	
	x = 0
	while x != 1:
		loopSpeed = input("How many seconds until looping to the next playing status(default: 300)> ")
		if loopSpeed == '':
			loopSpeed = 300
		else:
			try:
				loopSpeed = int(loopSpeed)
				x = 1
			except:
				print("{0} is not a valid number?".format(loopSpeed))

	return token, prefix, pm, defaultChannel, loopSpeed

def configGenerate():
	file = open("config.json", "w+")
	token, prefix, pm, defaultChannel, loopSpeed = firstConfig()
	data = {"token": token, "prefix": prefix, "pm": pm, "defaultChannel": defaultChannel, "loopSpeed": loopSpeed}
	#file.write("Token:\n{0}\n\nprefix (default is $)\n{1}\n\nPrivate message the help text (can be True of False, default is True)\n{2}\n\nDefault channel name\n{3}".format(token, prefix, pm, defaultChannel))
	#file.close()
	json.dump(data, file, indent=2)
	
def configLaunch():
	try:
		config = json.load(open("config.json"))
		return config
	except:
		regen = input("Something went wrong when reading the config file. Would you like to regenerate the file?(y/N)> ")
		if regen.lower() == 'y':
			confirm = input("Are you sure you want to continue? This can not be undone(y/N)> ")
			if confirm.lower() == 'y':
				configGenerate()
				print("The bot now needs to be restarted...")
				exit()
			else:
				print("Config file has not been regenerated. Check it for any errors")
				exit()
		else:
			print("Config file has not been regenerated. Check it for any errors")
			exit()

#SERVER COMMANDS
def serverCommands():
	while 1==1:
		scommand = input("> ")
		if scommand.lower() == "quit":
			os._exit(1)
		if scommand.lower() == 'reload':
			reload()
		if scommand.lower() == 'help':
			print("Reload: used to reload cogs\nQuit: used to shutdown the bot\nHelp: used to show this text")

#token, prefix, pm, defaultChannel = configLaunch()
config = configLaunch()

bot = commands.Bot(command_prefix=config["prefix"], pm_help=config["pm"], command_not_found="Command {} not found. Did you type it correctly?")
client = discord.Client()

#gets list of cogs in the cogs folder at startup
extensions = []
for x in os.listdir("cogs"):
	if str(x[(len(x)-3):]) == ".py":
		extensions.append(x)



if __name__ == '__main__':
	for x in extensions:
		name = ('cogs.' + x[:-3])
		try:
			bot.load_extension(name)
		except:
			print(f"Error loading {x}", file=sys.stderr)
			traceback.print_exc()
			
def reload():
	for x in extensions:
		name = ('cogs.' + x[:-3])
		try:
			bot.unload_extension(name)
			bot.load_extension(name)
		except:
			print("Error loading {0}".format(x), file=sys.stderr)
			traceback.print_exc()
			
@bot.event
async def on_ready():
	reload()
	global totalGuilds
	totalGuilds = 0
	for x in bot.guilds:
		totalGuilds += 1
	print('CaffeineBot connected through user {0}'.format(bot.user.name))
	#await bot.change_presence(game=discord.Game(name="{0}help".format(config["prefix"])))
	bot.loop.create_task(loopPlaying(bot, config["loopSpeed"]))
	t = Thread(target=serverCommands)
	t.start()
		
@bot.event
async def on_guild_join(guild):
	global totalGuilds
	totalGuilds += 1
	
@bot.event
async def on_guild_leave(guild):
	totalGuilds -= 1
		
@bot.event
async def on_member_join(member):
	guildID = member.guild.id
	userID = member.id
	conn = sqlite3.connect("users.db")
	connection = conn.cursor()
	#connection.execute('''INSERT INTO guildUsers (guildID, userID) VALUES (?, ?)''', (guildID, userID))
	conn.close()
'''@bot.event
async def on_command_error(ctx, error):
	await ctx.send("There is no command called {0}".format(str(error)[9:-14]))'''
		
async def loopPlaying(bot, loopSpeed):
	while True:
		guildUpdateSpeed = int(loopSpeed / 10)
		await bot.change_presence(game=discord.Game(name="{0}help".format(config["prefix"])))
		await asyncio.sleep(loopSpeed)
		await bot.change_presence(game=discord.Game(name="Developed by qspitzer"))
		await asyncio.sleep(loopSpeed)
		await bot.change_presence(game=discord.Game(name="6a 75 73 74 20 6d 6f 6e 69 6b 61"))
		await asyncio.sleep(loopSpeed)
		for x in range(guildUpdateSpeed):
			await bot.change_presence(game=discord.Game(name="Currently on {0} guilds".format(totalGuilds)))
			await asyncio.sleep(10)
	
if not os.path.isfile("users.db"):
	open("users.db", "w+")

	
#bot.loop.create_task(loopPlaying(bot, config["loopSpeed"]))
bot.run(config["token"])
