import discord
from discord.ext import commands
import random
import os
import json
from random import randrange

client = commands.Bot(command_prefix = '.')
os.chdir(r'C:\Users\elias\OneDrive\Desktop\discord bot')


#Bot status message to determine if ready
@client.event
async def on_ready():
	print('Bot is ready.')

@client.event
async def on_member_join(member):
	with open('users.json', 'r') as f:
		users = json.load(f)

	await update_data(users, member)

	with open('users.json', 'w') as f:
		json.dump(users, f)


@client.event
async def on_message(message):
	with open('users.json', 'r') as f:
		users = json.load(f)

	await update_data(users, message.author)
	await add_experience(users, message.author, 5)
	await level_up(users, message.author, message.channel)

	with open('users.json', 'w') as f:
		json.dump(users, f)

async def update_data(users, user):
	if not user.id in users:
		users[user.id] = {}
		users[user.id]['experience'] = 0
		users[user.id]['level'] = 1

async def add_experience(users, user, exp):
	users[user.id]['experience'] += exp

async def level_up(users, user, channel):
	experience = users[user.id]['experience']
	lvl_start = users[user.id]['level']
	lvl_end = int(experience ** (1/4))

	if lvl_start < lvl_end:
		await client.send_message(channel, '{} has leveled up to level {}'.format(user.mention, lvl_end))
		users[user.id]['level'] = lvl_end

#Provides output to the console when a new member has joined the server
@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

#Provides output to the console when a member has left the server
@client.event
async def on_member_remove(member):
	print(f'{member} has left a server.')


# @client.command()
# async def ping(ctx):
# 	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')
# Interactive 8Ball Game 

#8-Ball Game Created using python
@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
	reponses =''
	responses = ['– It is certain.',
					'– It is decidedly so.',
					'– Without a doubt.',
					'– Yes – definitely',
					'– You may rely on it.',
					'– As I see it, yes.',
					'– Most likely.',
					'– Outlook good.',
					'– Yes.',
					'– Signs point to yes.',
					'– Reply hazy try again.',
					'– Ask again later.',
					'– Better not tell you now.',
					'– Cannot predict now.',
					'– Concentrate and ask again.'
					'– Don’t count on it.',
					'– My reply is no.',
					'– My sources say no.',
					'– Outlook not so good.',
					'– Very doubtful.']
		await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def randomNumber(ctx, min, max):
	await ctx.send(f'Random Number from {min} to {max}: {(int(random.uniform(int(min), int(max),)))}')

@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)

client.run('')
