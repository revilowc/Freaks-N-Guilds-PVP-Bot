import discord
from discord.ext import commands

import os
import time
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('bottoken')

intents = discord.Intents.all()
client = commands.Bot(
    command_prefix=commands.when_mentioned_or('!'),
    activity=discord.Game(name="Freaky Battles"),
    intents=intents,
    help_command=None,
    case_insensitive=True)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_interaction(interaction):
    await client.process_application_commands(interaction)


@commands.is_owner()
@client.command(pass_context=True)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.reply(embed=discord.Embed(
        description=f"**Loaded '{extension}' cog**", color=0x000ff))
    time.sleep(1)
    await ctx.channel.purge(limit=2)


@commands.is_owner()
@client.command(pass_context=True)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

    await ctx.reply(embed=discord.Embed(
        description=f"**Unloaded '{extension}' cog**", color=0x000ff))
    time.sleep(1)
    await ctx.channel.purge(limit=2)


@commands.is_owner()
@client.command(pass_context=True)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

    await ctx.reply(embed=discord.Embed(
        description=f"**Reloaded '{extension}' cog**", color=0x000ff))
    time.sleep(1)
    await ctx.channel.purge(limit=2)

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
