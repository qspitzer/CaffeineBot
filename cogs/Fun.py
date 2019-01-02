import discord
from discord.ext import commands
import random
#import urllib.request as uReq
import requests
from PIL import Image, ImageDraw, ImageOps
import io, os
import asyncio
import glob
import sqlite3
import moviepy.editor as mpy

class Fun():
	def __init__(self, bot):
		self.bot = bot
	
	#fruits
	fruit = {
		1 : ":pear:",
		2 : ":lemon:",
		3 : ":cherries:",
		4 : ":grapes:",
		5 : ":watermelon:",
		6 : ":banana:",
		7 : ":kiwi:"
	}
	
	@commands.command(name='slots')
	async def slots(self, ctx, amount = 10):
		"""Just like Vegas!"""
		guildID = ctx.message.guild.id
		fruit1 = random.randint(1, 7)
		fruit2 = random.randint(1, 7)
		fruit3 = random.randint(1, 7)
		user = ctx.message.author
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		connectionB.execute('''SELECT money FROM economy WHERE userID=? AND guildID = ?''', (user.id, guildID))
		tmp = connectionB.fetchone()
		currentMoney = tmp[0]
		#guildID = ctx.message.guild
		try:
			amount = int(amount)
			if amount <= currentMoney and amount > 0:
				if fruit1 == fruit2 and fruit2 == fruit3:
					await bot.say("[{0} | {1} | {2}]\n**{3}** gambled and won".format(self.fruit[fruit1], self.fruit[fruit2], self.fruit[fruit3], user.name))
					connectionB.execute('''UPDATE economy SET money=(money+?) WHERE userID=? AND guildID=?''', (amount, user.id, guildID))
					connB.commit()
				elif fruit1 == fruit2 or fruit2 == fruit3 or fruit3 == fruit1:
					await ctx.send("[{0} | {1} | {2}]\n**{3}** almost won".format(self.fruit[fruit1], self.fruit[fruit2],self.fruit[fruit3], user.name))
				else:
					await ctx.send("[{0} | {1} | {2}]\n**{3}** gambled and lost".format(self.fruit[fruit1], self.fruit[fruit2], self.fruit[fruit3], user.name))
					connectionB.execute('''UPDATE economy SET money=(money-?) WHERE userID=? AND guildID=?''', (amount, user.id, guildID))
					connB.commit()
			elif amount <= 0:
				await ctx.send("{0} is not a valid number!".format(amount))
			else:
				await ctx.send("You do not have {0} monies!".format(amount))
		except:
			await ctx.send("{0} is not a valid number!".format(amount))
		connB.close()
				
	@commands.command(name='suckerPunch')		
	async def suckerPunch(self, ctx, user: str):
		'''potentially KO someone'''

		if user[0] == "@":
			uname = discord.utils.get(ctx.message.guild.members, name=user[1:-5])
		else:
			uname = discord.utils.get(ctx.message.guild.members, name=user)
		author = ctx.message.author
		uID = uname.id
		aID = author.id
		guildID = ctx.message.guild.id
		whoPunch = random.randint(1, 10)
		#whoPunch = 10
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		
		#uname = str(uname)
		#author = str(ctx.message.author)
		if uname == author:
			await ctx.send("You can't sucker punch yourself dummy")
		elif uname != None:
			connection.execute('''SELECT money FROM economy WHERE userID=? AND guildID=?''', (uID, guildID))
			uMoney = connection.fetchone()
			connection.execute('''SELECT money FROM economy WHERE userID=? AND guildID=?''', (aID, guildID))
			aMoney = connection.fetchone()
		
			uMoney = int(uMoney[0])
			aMoney = int(aMoney[0])

			if whoPunch in range(1, 5):
				await ctx.send("{0} sucker punched {1}".format(author.name, uname.name))
			elif whoPunch in range(5, 9):
				await ctx.send("{0} tried to sucker punch {1}, but {1} sucker punched {0}".format(author.name, uname.name))
			elif whoPunch == 9:
				await ctx.send("{0} sucker punched {1} and took 1/2 of {1}'s money".format(author.name, uname.name))
				newMoney = (uMoney/2)
				connection.execute('''UPDATE economy SET money=(money/2) WHERE userID=? AND guildID=?''', (uID, guildID))
				connection.execute('''UPDATE economy SET money=(money+?) WHERE userID=? AND guildID=?''', (newMoney, aID, guildID))
				conn.commit()
			elif whoPunch == 10:
				await ctx.send("{0} tried to sucker punch {1}, but was beaten and robbed by {1} (ya dun goofed {0})".format(author.name, uname.name))
				newMoney = (aMoney/2)
				connection.execute('''UPDATE economy SET money=(money/2) WHERE userID=? AND guildID=?''', (aID, guildID))
				connection.execute('''UPDATE economy SET money=(money+?) WHERE userID=? AND guildID=?''', (newMoney, uID, guildID))
				conn.commit()
		else:
			await ctx.send("There is no one named {0}".format(user))
		conn.close()
		
class Event():
	def __init__(self, bot):
		self.bot = bot
		
	'''def on_ready(self):
		try:
			for x in ctx.guilds:
				try:
					await self.bot.'''
		
		
def setup(bot):
	bot.add_cog(Fun(bot))
	bot.add_cog(Event(bot))
