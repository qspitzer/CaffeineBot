import discord
from discord.ext import commands
from discord.ext.commands import Bot
import sqlite3

class Regen():
	def __init__(self, bot):
		self.bot = bot

	def Economy(self):
		connB = sqlite3.connect("users.db")
		connectionB = connB.cursor()
		connectionB.execute('''CREATE TABLE IF NOT EXISTS economy(guildID INTEGER, userID INTEGER, user TEXT NOT NULL, level INTEGER DEFAULT 1, exp INTEGER DEFAULT 0, money INTEGER DEFAULT 50, turkies INTEGER DEFAULT 0, ducks INTEGER DEFAULT 0, chickens INTEGER DEFAULT 0, flyingPigs INTEGER DEFAULT 0)''')
		for x in self.bot.guilds:
			for y in x.members:
				connectionB.execute('''INSERT INTO economy (guildID, userID, user) VALUES (?, ?, ?)''', (x.id, y.id, y.name))
				connB.commit()
		connB.close()
	
def setup(bot):
	Regen(bot).Economy()
	bot.add_cog(Regen(bot))
	