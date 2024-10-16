from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from models.attribute import Attribute
import models.stats
from models.character import Character

from services import charactersvc
from util.errors import CharacterException

async def setup(bot):
    await bot.add_cog(CharacterCog(bot))

class CharacterCog(commands.GroupCog, name='character', description='Character commands'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.user_menu = app_commands.ContextMenu(callback=self.sheet_user, name="Show active character")
        self.bot.tree.add_command(self.user_menu)

    async def sheet_user(self, inter: discord.Interaction, member: discord.Member) -> None:
        active_character = charactersvc.get_active_character_by_user_id(member.id)
        if active_character is None:
            await inter.response.send_message('That user does not have an active character.')
            return

        embed = discord.Embed(
            title=member.name,
            description=f"{member.mention}'s active character is: {active_character.name}", color=member.color
        )
        embed.set_thumbnail(url=member.display_avatar)
        await inter.response.send_message(embed=embed)

    @app_commands.command(name="create", description="Creates a new character.")
    @app_commands.describe(charname="The character's name.")
    async def create_character(self, interaction: discord.Interaction, charname: str) -> None:
        charactersvc.create_character(interaction.user.id, charname)
        await interaction.response.send_message('Character created.')

    @app_commands.command(name="activate", description="Activates an existing character.")
    @app_commands.describe(charname="The character's name.")
    async def activate_character(self, interaction: discord.Interaction, charname: str) -> None:
        if charactersvc.activate_character(interaction.user.id, charname):
            await interaction.response.send_message('Character activated.')
            return

        await interaction.response.send_message('Failed to activate character.')

    async def show_sheet_by_name(self, interaction: discord.Interaction, character_name: str) -> None:
        matching_character = charactersvc.find_character_by_name(character_name)

        if matching_character is None:
            await interaction.response.send_message('Could not find a character with that name.')
            return

        await interaction.response.send_message(f"Here's the sheet for {matching_character.name}.",
                                                embed=self.format_sheet(interaction.user, matching_character))

    def get_skills_sheet_by_attribute(self, character: Character, attribute: Attribute) -> str:
        result = ''
        for skill in models.stats.get_skills(attribute):
            result += f"{models.stats.get_pretty_name(skill)}: {character.get_effective_skill(skill)}\n"
        return result

    def format_sheet(self, member: discord.Member, character: Character) -> discord.Embed:
        embed = discord.Embed(title=character.name, description=character.description, color=member.color)

        for attribute in Attribute.__members__.values():
            embed.add_field(name=f'{models.stats.get_pretty_name(attribute)}: {character.get_attribute(attribute)}',
                            value=self.get_skills_sheet_by_attribute(character, attribute))

        return embed

    @app_commands.command(name="sheet", description="Display your active character's sheet.")
    @app_commands.describe(
        other_user="Optionally view another user's active character.",
        character_name="Optionally find a character sheet using the character's name.")
    async def show_sheet(self,interaction: discord.Interaction, other_user: Optional[discord.Member], character_name: Optional[str]) -> None:
        if character_name:
            return await self.show_sheet_by_name(interaction, character_name)

        user_id = other_user.id if other_user else interaction.user.id
        character = charactersvc.get_active_character_by_user_id(user_id)
        if character is None:
            await interaction.response.send_message("No character found.")
            return

        await interaction.response.send_message(f"Here's the sheet for {character.name}.",
                                                embed=self.format_sheet(interaction.user, character))

    @app_commands.command(name="list", description="Display a list of all of your characters.")
    @app_commands.describe(other_user="Optionally view another user's characters. If ommitted, display your own characters.")
    async def list_characters(self, interaction: discord.Interaction, other_user: Optional[discord.Member]) -> None:
        user_id = other_user.id if other_user else interaction.user.id
        character_list = charactersvc.get_characters_owned_by_user(user_id)

        if character_list is None:
            await interaction.response.send_message("There aren't any characters to show!")
            return

        character_names = ', '.join(o.name for o in character_list)

        await interaction.response.send_message(f"Characters: {character_names}.")

    @app_commands.command(name="setattribute", description="Set the value of one of your character's attributes.")
    @app_commands.describe(attribute_name="The name of the attribute to edit.", value="An integer to set the attribute's value to.")
    async def set_attribute(self, interaction: discord.Interaction, attribute_name: str, value: int) -> None:
        try:
            charactersvc.set_attribute(interaction.user.id, attribute_name, value)
            await interaction.response.send_message("Attribute successfully set.")
        except CharacterException as e:
            await interaction.response.send_message(f"An error occurred while setting the attribute: {e}")

    @app_commands.command(name="setskill", description="Set the value of one of your character's skills.")
    @app_commands.describe(skill_name="The name of the skill to edit.", value="An integer to set the skill's value to.")
    async def set_skill(self, interaction: discord.Interaction, skill_name: str, value: int) -> None:
        try:
            charactersvc.set_skill(interaction.user.id, skill_name, value)
            await interaction.response.send_message("Skill successfully set.")
        except CharacterException as e:
            await interaction.response.send_message(f"An error occurred while setting the skill: {e}")

    @set_attribute.autocomplete("attribute_name")
    async def attribute_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.attribute_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]

    @set_skill.autocomplete("skill_name")
    async def skill_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.skill_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]
