#!/usr/bin/env python3

import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension(name='cogs.charactercmds')
    await bot.load_extension(name='cogs.rollcmds')
    await bot.load_extension(name='cogs.itemcmds')

    await bot.tree.sync()
    print(f'We have logged in as {bot.user}')

bot.run(os.environ['BALLROOM_TOKEN'])
