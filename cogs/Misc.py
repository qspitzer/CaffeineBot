import discord
from discord.ext import commands
import asyncio
import requests
from bs4 import BeautifulSoup

class Misc():
	def __init__(self, bot):
		self.bot = bot
		#self.defaultChannel = defaultChannel
	@commands.command()
	async def clear(self, ctx, number: int):
		'''Clears previous messages'''
		if ctx.message.author == ctx.guild.owner or ctx.message.author.id == 274271139595812886:
			number = int(number) #Converting the amount of messages to delete to an integer
			counter = 0
			cycles, overflow = divmod(number + 1, 100)
			for z in range(cycles):
				async for x in ctx.channel.history():
					if counter <= 100:
						await x.delete()
						counter += 1
						await asyncio.sleep(1.2)
				#await ctx.send("cycle done")
			for y in range(overflow): #problems
				async for x in ctx.channel.history():
					if counter <= ((cycles * 100) + (overflow - 1)):
						await x.delete()
						counter += 1
						await asyncio.sleep(1.2)
			
			#await ctx.send(counter)
		else:
			await ctx.send("You need to be the owner to do that!")
		
	@commands.command()
	async def ping(self, ctx):
		'''A useless command'''
		await ctx.send("Pong!")

	@commands.command()
	async def pong(self, ctx):
		'''An even more useless command'''
		await ctx.send("Ping!")
		
	@commands.command()
	async def dong(self, ctx):
		'''an extremly useless command'''
		await ctx.send("Ding!")
	@commands.command()
	async def ding(self, ctx):
		'''the most useless command of them all'''
		await ctx.send("Dong!")
	@commands.command()
	@commands.has_role("test")
	async def test(self, ctx):
		ctx.send("Yes")
	
def setup(bot):
	bot.add_cog(Misc(bot))
