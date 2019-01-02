import discord
from discord.ext import commands
import sqlite3
import os
import asyncio
from datetime import datetime

#ADD FLYING PIGS, FP's WILL BE SIMILAR TO STOCKS, BUY AT ONE PRICE, SELL IT TO OTHER USERS FOR MORE MONEY

conn = None
connection = None
FPSale = {}

def dumbReload(bot):
	bot.unload_extension("cogs.Economy")
	bot.load_extension("cogs.Economy")

class Economy():
	def __init__(self, bot):
		self.bot = bot
		self.check = 0
		
	@commands.command(name='stats')
	async def stats(self, ctx):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		user = ctx.message.author
		userID = ctx.message.author.id
		guildID = ctx.message.guild.id
		connection.execute('''SELECT * FROM economy WHERE userID=? AND guildID=?''', (userID, guildID))
		userInfo = connection.fetchone()
		#await bot.say("```{0}```".format(userInfo[0]))
		#message = ("```User: {0}\nID: {1}\nLevel: {2}\nExp: {3}\nMoney: {4}\nTurkies: {5}\nDucks: {6}\nChickens: {7}```".format(userInfo[1], userInfo[0], userInfo[2], userInfo[3], userInfo[4], userInfo[5], userInfo[6], userInfo[7]))
		e = discord.Embed(title="**{0}'s {1} Stats**".format(user.name, ctx.message.guild), colour=0x9b0000)
		e.add_field(name="Money", value=userInfo[5])
		e.add_field(name="Turkies", value=userInfo[6])
		e.add_field(name="Ducks", value=userInfo[7])
		e.add_field(name="Chickens", value=userInfo[8])
		e.add_field(name="Flying Pigs", value=userInfo[9])
		await user.send(embed = e)
		conn.close()
		
	@commands.command(name='sell')
	@commands.guild_only()
	async def sellFP(self, ctx, amount, price):
		'''Sell your flying pigs!'''
		global FPSale
		user = ctx.message.author
		guildID = ctx.message.guild.id
		try:
			amount = int(amount)
			try: 
				price = int(price)
				if amount > 0 and price > 0:
					userID = ctx.message.author.id
					connB = sqlite3.connect("users.db")
					connectionB = connB.cursor()
					connectionB.execute('''SELECT flyingPigs FROM economy WHERE userID=? AND guildID=?''', (userID, guildID))
					tmp = connectionB.fetchone()
					FPAmount = tmp[0]
					if FPAmount >= amount:
						minute = (datetime.now().minute + 2)
						if minute == 60:
							minute = 0
						if minute == 60:
							minute = 1
						experation = ("{:02d}".format(minute))
						
						present = 0
						for x in FPSale:
							if x[0] == user.id:
								present = 1
								break
							
						if present != 1:
							idExperation = (user.id, experation)
							amountPrice = (amount, price)
							FPSale[idExperation] = amountPrice
						else:
							await ctx.send("You already put up an offer {0}!".format(user.mention))
					else:
						await ctx.send("You don't have {0} flying pigs!".format(amount))
							
				if price <= 0:
					await ctx.send("{0} is not a valid price!".format(price))
				if amount <= 0:
					await ctx.send("{0} is not a valid amount!".format(amount))
				if self.check != 1:
					self.check = 1
					self.bot.loop.create_task(FPExpire(self.bot))
			except:
				await ctx.send("{0} is not a valid price!".format(price))
		except:
			await ctx.send("{0} is not a valid amount!".format(amount))
		connB.close()
	@commands.command(name='offers')
	@commands.guild_only()
	async def FPOffers(self, ctx):
		global FPSale
		user = ctx.message.author
		e = discord.Embed(title="Offers")
		if len(FPSale) > 0:
			for x in FPSale:
				#await ctx.send(x)
				tmp = FPSale[x]
				tmpUser = discord.utils.get(ctx.message.guild.members, id=x[0])
				e.add_field(name=tmpUser.name, value="Selling {0} flying pigs for {1}".format(tmp[0], tmp[1]))
		else:
			e.add_field(name="No offers at this time", value="come back later")
		await user.send(embed=e)
		#await ctx.send(self.FPSale)
		
	@commands.command(name='buy')
	@commands.guild_only()
	async def FPSale(self, ctx, user):
		global FPSale
		#global pause
		#pause = 1
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		currentUser = ctx.message.author
		offerUser = discord.utils.get(ctx.guild.members, name=user)
		guildID = ctx.message.guild.id
		connectionB.execute('''SELECT money FROM economy WHERE userID=? AND guildID=?''', (currentUser.id, guildID))
		tmp = connectionB.fetchone()
		currentMoney = tmp[0]
		valid = 0
		offerKey = None
		for x in FPSale:
			if x[0] == offerUser.id:
				valid = 1
				break
		if offerUser != None and valid == 1:
			for x in FPSale:
				if x[0] == offerUser.id:
					offerKey = x
					break
			offerValue = FPSale[offerKey]
			if offerValue[1] <= currentMoney:
				pigs = offerValue[0]
				connectionB.execute('''UPDATE economy SET money=(money-?), flyingPigs=(flyingPigs+?) WHERE userID=? AND guildID=?''', (offerValue[1], pigs, currentUser.id, guildID))
				connectionB.execute('''UPDATE economy SET money=(money+?), flyingPigs=(flyingPigs-?) WHERE userID=? AND guildID=?''', (offerValue[1], pigs, offerUser.id, guildID))
				connB.commit()
				del FPSale[x]
				
			else:
				await ctx.send("You do not have enought money to complete the purchase!")
			
		else:
			await ctx.send("{0} has not offered anything!")
		connB.close()
		#pause = 0
		
	@commands.command(name="FPUpdate", hidden=True)
	async def FPUpdate(self, ctx, user, value):
		if ctx.message.author.id == 274271139595812886:
			value = int(value)
			user = discord.utils.get(ctx.guild.members, name=user)
			connB = sqlite3.connect("users.db")
			connectionB = connB.cursor()
			guildID = ctx.message.guild.id
			connectionB.execute('''UPDATE economy SET flyingPigs=? WHERE userID=? AND guildID=?''', (value, user.id, guildID))
			connB.commit()
			connB.close()
		else:
			await ctx.send("No")

	@commands.group()
	async def convert(self, ctx):
		'''convert money to birds'''
		if ctx.invoked_subcommand is None:
			await ctx.send("Usage: convert conversions/money/chickens/ducks/turkies (money/chickens/ducks/turkies) (number of birds)")
			
	@convert.command(name='conversions')
	async def _bot(ctx):
		await ctx.send("```3 chickens = 1 duck\n2 ducks = 1 turkey\n8 monies = 1 chicken\n24 monies = 1 duck\n48 monies = 1 turkey```")

	@convert.command(name='money')
	async def _bot(ctx, conv: str, amt = 1):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		userID = ctx.message.author.id
		converties = ["chickens", "ducks", "turkies"]
		guildID = ctx.message.guild.id
		connection.execute('''SELECT money FROM economy WHERE userID=? AND guildID=?''', (userID, guildID))
		currentMoney = connection.fetchone()
		currentMoney = int(currentMoney[0])
		try:
			amt = int(amt)
			if amt >= 1:
				if conv in converties:
					if conv == converties[0]:
						if (amt*8) <= currentMoney:
							m2c = (amt*8)
							connection.execute('''UPDATE economy SET money=(money - ?), chickens=(chickens + ?) WHERE userID = ? AND guildID = ?''', (m2c, amt, userID, guildID))
							conn.commit()
						else:	
							await ctx.send("You do not have enough money to get that many chickens.")
					elif conv == converties[1]:
						if (amt*24) <= currentMoney:
							m2d = (amt*24)
							connection.execute('''UPDATE economy SET money=(money - ?), ducks=(ducks + ?) WHERE userID = ? AND guildID=?''', (m2d, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough money to get that many ducks.")
					elif conv == converties[2]:
						if (amt*48) <= currentMoney:
							m2t = (amt*48)
							connection.execute('''UPDATE economy SET money=(money-?), turkies=(turkies+?) WHERE userID = ? AND guildID = ?''', (m2t, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough money to get that many turkies.")
				else:
					await ctx.send("You can't convert money to {0}".format(conv))
			else:
				await ctx.send("You can't convert money to nothing")
		except:
			await ctx.send("{0} is not a valid number!".format(amt))
		conn.close()
	
	@convert.command(name='chickens')
	async def _bot(ctx, conv: str, amt = 1):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		userID = ctx.message.author.id
		converties = ["money", "ducks", "turkies"]
		guildID = ctx.message.guild.id
		connection.execute('''SELECT chickens FROM economy WHERE userID=? AND guildID=?''', (userID, guildID))
		currentChickens = connection.fetchone()
		currentChickens = int(currentChickens[0])
		try:
			amt = int(amt)
			if amt >= 1:
				if conv in converties:
					if conv == converties[0]:
						if amt <= currentChickens:
							c2m = (amt*8)
							connection.execute('''UPDATE economy SET money=(money + ?), chickens=(chickens - ?) WHERE userID = ? AND guildID = ?''', (c2m, amt, userID, guildID))
							conn.commit()
						else:	
							await ctx.send("You do not have enough chickens to do that.")
					elif conv == converties[1]:
						if (amt*2) <= currentChickens:
							c2d = (amt*2)
							connection.execute('''UPDATE economy SET chickens=(chickens-?), ducks=(ducks+?) WHERE userID=? AND guildID = ?''', (c2d, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough chickens to do that.")
					elif conv == converties[2]:
						if (amt*6) <= currentChickens:
							c2t = (amt*6)
							connection.execute('''UPDATE economy SET chickens=(chickens-?), turkies=(turkies+?) WHERE userID=? AND guildID=?''', (c2t, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough chickens to do that.")
				else:
					await ctx.send("You can't convert chickens to {0}".format(conv))
			else:
				await ctx.send("You can't convert chickens to nothing")
		except:
			await ctx.send("{0} is not a valid number!")
		conn.close()
	@convert.command(name='ducks')
	async def _bot(ctx, conv: str, amt = 1):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		userID = ctx.message.author.id
		converties = ["money", "chickens", "turkies"]
		guildID = ctx.messae.guild.id
		connection.execute('''SELECT ducks FROM economy WHERE userID=? AND guildID = ?''', (userID, guildID))
		currentDucks = connection.fetchone()
		currentDucks = int(currentDucks[0])
		try:
			amt = int(amt)
			if amt >= 1:
				if conv in converties:
					if conv == converties[0]:
						if amt <= currentDucks:
							d2m = (amt*24)
							connection.execute('''UPDATE economy SET money=(money+?), ducks=(ducks-?) WHERE userID=? AND guildID=?''', (d2m, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough ducks to do that.")
					elif conv == converties[1]:
						if amt <= currentDucks:
							d2c = (amt*3)
							connection.execute('''UPDATE economy SET chickens=(chickens+?), ducks=(ducks-?) WHERE userID=? AND guildID=?''', (d2c, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough ducks to do that.")
					elif conv == converties[2]:
						if amt <= currentDucks:
							d2t = (amt*2)
							connection.execute('''UPDATE economy SET turkies=(turkies+?), ducks=(ducks-?) WHERE userID=? AND guildID=?''', (amt, d2t, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough ducks to do that.")
				else:
					await ctx.send("You can't convert ducks to {0}".format(conv))
			else:
				await ctx.send("You can't convert ducks to nothing")
		except:
			await ctx.send("{0} is not a valid number!".format(amt))
		conn.close()
	@convert.command(name='turkies')
	async def _bot(ctx, conv: str, amt = 1):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		userID = ctx.message.author.id
		converties = ["money", "chickens", "ducks"]
		guildID = ctx.message.guild.id
		connection.execute('''SELECT turkies FROM economy WHERE userID=? AND guildID = ?''', (userID, guildID))
		currentTurkies = connection.fetchone()
		currentTurkies = int(currentTurkies[0])
		try:
			amt = int(amt)
			if amt >= 1:
				if conv in converties:
					if conv == converties[0]:
						if amt <= currentTurkies:
							t2m = (amt*48)
							connection.execute('''UPDATE economy SET money=(money+?), turkies=(turkies-?) WHERE userID=? AND guildID=?''', (t2m, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough turkies to do that.")
					elif conv == converties[1]:
						if amt <= currentTurkies:
							t2c = (amt*6)
							connection.execute('''UPDATE economy SET chickens=(chickens+?), turkies=(turkies-?) WHERE userID=? AND guildID=?''', (t2c, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough turkies to do that.")
					elif conv == converties[2]:
						if amt <= currentTurkies:
							t2d = (amt*2)
							connection.execute('''UPDATE economy SET ducks=(ducks+?), turkies=(turkies-?) WHERE userID=? AND guildID=?''', (t2d, amt, userID, guildID))
							conn.commit()
						else:
							await ctx.send("You do not have enough turkies to do that.")
				else:
					await ctx.send("You can't convert turkies to {0}".format(conv))
			else:
				await ctx.send("You can't convert turkies to nothing")
		except:
			await ctx.send("{0} is not a valid number!".format(amt))		
		conn.close()
		
	"""@commands.command(name="bankrupt")
	async def bankrupt(self, ctx):
		conn = sqlite3.connect("users.db")
		connection = conn.cursor()
		selectedBird = random.randint(1,3)
		userID = ctx.message.author.id
		guildID = ctx.message.guild.id
		if selectedBird == 1:
			connection.execute('''UPDATE economy SET money=0, turkies=0 WHERE userID=? AND guildID=?''', (userID, guildID))
		elif selectedBird == 2:
			connection.execute('''UPDATE economy SET money=0, ducks=0 WHERE userID=? AND guildID=?''', (userID, guildID))
		elif selectedBird == 3:
			connection.execute('''UPDATE economy SET money=0, chickens=0 WHERE userID=? AND guildID=?''', (userID, guildID))
		conn.commit()
		conn.close()
		await ctx.send("{0} has just declaired bankruptcy".format(ctx.message.author.mention))"""
		
		
		
#remove old offers
async def FPExpire(bot):
	global FPSale
	#global pause
	while True:
		#if pause != 1:
		remove = []
		await asyncio.sleep(10)
		if len(FPSale) > 0:
			currentTime = "{:02d}".format(datetime.now().minute)
			for x in FPSale:
				if x[1] == currentTime:
					remove.append(x)
			for x in remove:
				del FPSale[x]
			
		else:
			pass
		
		
def usersCheck(bot):
	conn = sqlite3.connect("users.db")
	connection = conn.cursor()
	connection.execute('''SELECT userID FROM economy''')
	all_id = connection.fetchall()
	if len(all_id) != 0:
		for x in bot.guilds:
			for y in x.members:
				if y.id not in all_id:
					try:
						connection.execute('''INSERT INTO economy (guildID, userID, user) VALUES (?, ?, ?)''', (x.id, y.id, y.name)) 
						conn.commit()
					except:
						pass
	else:
		for x in bot.guilds:
			for y in x.members:
				try:
					connection.execute('''INSERT INTO economy (guildID, userID, user) VALUES (?, ?, ?)''', (x.id, y.id, y.name))
					conn.commit()
				except:
					pass	
	conn.close()
	asyncio.sleep(1)

class Event():
	def __init__(self, bot):
		self.bot = bot
		
	async def on_ready(self):
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		connectionB.execute('''CREATE TABLE IF NOT EXISTS economy(guildID INTEGER, userID INTEGER, user TEXT NOT NULL, level INTEGER DEFAULT 1, exp INTEGER DEFAULT 0, money INTEGER DEFAULT 50, turkies INTEGER DEFAULT 0, ducks INTEGER DEFAULT 0, chickens INTEGER DEFAULT 0, flyingPigs INTEGER DEFAULT 1)''')
		connB.commit()
		connB.close()
		usersCheck(self.bot)
		self.bot.loop.create_task(addMoney(self.bot))
		#self.bot.loop.create_task(Economy(self.bot).FPExpire())
		#currentTime = "{:02d}".format(datetime.now().minute)
		#print("{0}, {1}".format(Economy(self.bot).FPSale, currentTime))
		
	async def on_member_join(self, member):
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		connectionB.execute('''INSERT INTO economy (guildID, userID, user) VALUES (?, ?, ?)''', (member.guild.id, member.id, member.name))
		connB.commit()
		connB.close()
		
	async def on_guild_join(self, guild):
		print(guild.id)
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		#user = discord.utils.get(guild.members, id=274271139595812886)
		#user.send(guild.members)
		for x in guild.members:
			print(x)
			connectionB.execute('''INSERT INTO economy (guildID, userID, user) VALUES (?, ?, ?)''', (guild.id, x.id, x.name))
			connB.commit()
		connB.close()
		
	async def on_guild_remove(self, guild):
		guildID = guild.id
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		connectionB.execute('''DELETE FROM economy WHERE guildID=?''', (guildID,))
		
#money add		
async def addMoney(bot):
	await bot.wait_until_ready()
	#print("hello")
	asyncio.sleep(1)
	while not bot.is_closed():
		connA = sqlite3.connect("users.db")
		connectionA = connA.cursor()
		for x in bot.guilds:
			#print("hello")
			for y in x.members:
				if y.status.online:
					#print("hi")
					userID = y.id
					connectionA.execute('''SELECT money FROM economy WHERE userID=? AND guildID=?''', (userID, x.id))
					currentAmount = connectionA.fetchone()
					connectionA.execute('''SELECT level FROM economy WHERE userID=? AND guildID=?''', (userID, x.id))
					level = connectionA.fetchone()
					
					multiplier = level[0]
					newAmount = (int(currentAmount[0]) + (10*multiplier))
					connectionA.execute('''UPDATE economy SET money=? WHERE userID=? AND guildID=?''', (newAmount, userID, x.id))
					connA.commit()
		connA.close()
		await asyncio.sleep(1800)
		

def setup(bot):
	bot.add_cog(Event(bot))
	bot.add_cog(Economy(bot))
	#print(Economy(bot).FPSale)
	#bot.loop.create_task(FPExpire(bot))
	#bot.loop.create_task(economyEventFunction(bot))
