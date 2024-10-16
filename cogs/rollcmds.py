from discord import Colour, app_commands
from discord.ext import commands

import discord

async def setup(bot):
    await bot.add_cog(RollCog(bot))

class RollCog(commands.GroupCog, name='roll', description='Roll commands'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="logic", description="Makes a Logic roll.")
    @app_commands.describe(body="The body of the message accompanying the roll.")
    async def roll_logic(self, interaction: discord.Interaction, body: str) -> None:
        embed = discord.Embed(title='Logic', description=body, color=Colour.blue())
        await interaction.response.send_message(embed=embed)
