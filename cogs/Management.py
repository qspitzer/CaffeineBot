import discord
from discord.ext import commands
import os, sys, traceback, asyncio
import requests
import sqlite3

class Management():
	def __init__(self, bot):
		self.bot = bot
	
	async def reloadCommand(self, channel, cog, userID, usage = 0):
	
		if userID == 274271139595812886:
			if cog == None:
				cogs = []
				for x in os.listdir("cogs"):
					if str(x[(len(x)-3):]) == '.py':
						cogs.append(x)
						
				if usage == 1:
					for cog in cogs:
						name = ('cogs.' + cog[:-3])
						try:
							self.bot.unload_extension(name)
						except:
							await channel.send("**ERROR:** could not reload {0}".format(name))
					os.remove("users.db")
					file = open("users.db", 'w+')
					file.close()
					for cog in cogs:
						name = ('cogs.' + cog[:-3])
						try:
							self.bot.load_extension(name)
						except:
							pass
							
				else:
					for cog in cogs:
						name = ('cogs.' + cog[:-3])
						try:
							self.bot.unload_extension(name)
							self.bot.load_extension(name)
						except:
							await channel.send("**ERROR:** could not reload {0}".format(name))
					await channel.send("**RELOAD COMPLETE**")
			else:
				if cog[:-(len(cog)-5)] == 'cogs.':
					name = cog
				else:
					name = ('cogs.' + cog)
				try:
					self.bot.unload_extension(name)
					self.bot.load_extension(name)
					await channel.send("**{0} RELOADED**".format(name))
				except:
					await channel.send("**ERROR:** could not reload {0}".format(name))
		else:
			await channel.send("Only qspitzer can do that!")
	
	
	@commands.command(name='load', hidden=True)
	@commands.guild_only()
	async def load(self, ctx, *, cog: str):
		if ctx.message.author.id == 274271139595812886:
			if cog[:-(len(cog)-5)] == 'cogs.':
				name = cog
			else:
				name = ('cogs.' + cog)
			try:
				self.bot.load_extension(name)
				await ctx.send("**Successfully loaded {0}**".format(name))
			except:
				await ctx.send("**ERROR:** could not load cog {0}".format(name))
		else:
			ctx.send("You need to be qspitzer to do that")
		
	@commands.command(name='unload', hidden=True)
	@commands.guild_only()
	async def unload(self, ctx, *, cog: str):
		if ctx.message.author.id == 274271139595812886:
			if cog[:-(len(cog)-5)] == 'cogs.':
				name = cog
			else:
				name = ('cogs.' + cog)
			try:
				self.bot.unload_extension(name)
			except:
				await ctx.send("**ERROR:** could not unload cog {0}".format(cog))
			else:
				await ctx.send("**Successfully unloaded {0}**".format(cog))
		else:
			await ctx.send("You need to be qspitzer do that")
	@commands.command(name='reload', hidden=True)
	@commands.guild_only()
	async def reload(self, ctx, cog = None):
		channel = ctx.message.channel
		userID = ctx.message.author.id
		await Management.reloadCommand(self, channel, cog, userID)
	
	
	@commands.command(name='cogAdd', hidden=True)
	async def cogAdd(self, ctx):
		userID = ctx.message.author.id
		if userID == 274271139595812886:
			#log = open("log.txt", "w+")
			count = 0
			async for message in ctx.channel.history():
				if count != 1:
					if not message.attachments:
						await ctx.send("You need to add a file to upload")
						count = 1
					elif message.attachments:
						tmp = message.attachments
						attachment = tmp[0]
						attURL = attachment.url
						downFile = requests.get(attURL).content
						path = ("cogs/" + attachment.filename)
						with open(path, "wb") as handel:
							handel.write(downFile)
						
						#await ctx.send(attachment.filename)
						count = 1
					else:
						await ctx.send("Error")
						count = 1
						'''atchmnt = ctx.message.attachments
						await ctx.send(atchmnt.filename)
						atchURL = atchmnt.url'''			
		else:
			await ctx.send("Only qspitzer can do that")
		
	@commands.command(name="dbRegen", hidden=True)
	async def dbRegen(self, ctx):
		cog = None
		channel = ctx.message.channel
		userID = ctx.message.author.id
		if userID == 274271139595812886:
			await Management.reloadCommand(self, channel, cog, userID, 1)
			await ctx.send("users.db has been recreated")
			#file.close()
			#connB.close()
		else:
			await ctx.send("Only qspitzer can do that")
	
def setup(bot):
	bot.add_cog(Management(bot))
