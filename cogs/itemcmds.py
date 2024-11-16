from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import models
from models.attribute import Attribute
from models.item import Item
from models.item_type import ItemType
from models.skill import Skill
from services import itemsvc
from util.errors import ItemException, PermissionException, StatException

async def setup(bot):
    await bot.add_cog(ItemCog(bot))

class ItemCog(commands.GroupCog, name='item', description='Item commands'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="create", description="Creates a new item.")
    @app_commands.describe(itemname="The items's name.",
                           itemdesc="The description of the item.",
                           itemtype="The type of the item. Can be Wearable, Consumable, or Misc.")
    async def create_item(self, interaction: discord.Interaction, itemname: str, itemdesc: str, itemtype: str) -> None:
        try:
            parsed_type = ItemType[itemtype.upper()]
        except KeyError:
            await interaction.response.send_message(f'Invalid item type given. Valid options are: {", ".join(ItemType.__members__.keys())}')
            return

        try:
            itemsvc.create_item(interaction.user.id, itemname, itemdesc, parsed_type)
        except ItemException as e:
            await interaction.response.send_message(f'Failed to create item. {e}')
            return

        await interaction.response.send_message('Item created.')

    @create_item.autocomplete("itemtype")
    async def itemtype_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = ItemType.__members__.keys()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]

    def format_sheet(self, member: discord.Member, item: Item) -> discord.Embed:
        embed = discord.Embed(title=item.name, description=item.description, color=member.color)
        embed.description = f'{item.description}\n\n'

        for effect in item.effects:
            plus_sign = ''
            if effect.value > 0:
                plus_sign = '+'
            embed.description += f'{plus_sign}{effect.value} {models.stats.get_pretty_name(effect.stat)}: {effect.stat_desc}\n'

        embed.set_image(url='https://goon.network/millerhighlife.png')

        return embed

    @app_commands.command(name="inspect", description="Show details about an item.")
    async def inspect_item(self, inter: discord.Interaction, item_name: str) -> None:
        item = itemsvc.find_item_by_name(item_name)
        if item is None:
            await inter.response.send_message('An item with that name could not be found.')
            return

        await inter.response.send_message(embed=self.format_sheet(inter.user, item))

    @app_commands.command(name="setattribute", description="Add an effect to an item that adjusts an Attribute.")
    @app_commands.describe(item_name="The name of the item to apply the effect to.",
                           attribute_name="The name of the attribute the effect applies to.",
                           value="An integer that will be added to the target character's attribute.",
                           stat_description="A short description detailing why the item applies this specific effect.")
    async def set_attribute(self, interaction: discord.Interaction, item_name: str, attribute_name: str, value: int, stat_description: str) -> None:
        try:
            itemsvc.set_attribute(interaction.user.id, item_name, attribute_name, value, stat_description)
            await interaction.response.send_message("Attribute successfully set.")
        except (ItemException, PermissionException, StatException) as e:
            await interaction.response.send_message(f"An error occurred while setting the attribute: {e}")

    @app_commands.command(name="setskill", description="Add an effect to an item that adjusts a Skill.")
    @app_commands.describe(item_name="The name of the item to apply the effect to.",
                           skill_name="The name of the skill the effect applies to.",
                           value="An integer that will be added to the target character's skill.",
                           stat_description="A short description detailing why the item applies this specific effect.")
    async def set_skill(self, interaction: discord.Interaction, item_name: str, skill_name: str, value: int, stat_description: str) -> None:
        try:
            itemsvc.set_skill(interaction.user.id, item_name, skill_name, value, stat_description)
            await interaction.response.send_message("Skill successfully set.")
        except (ItemException, PermissionException, StatException) as e:
            await interaction.response.send_message(f"An error occurred while setting the skill: {e}")

    @inspect_item.autocomplete("item_name")
    async def all_item_names_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = itemsvc.roughly_search_all_item_names(current)
        return [app_commands.Choice(name=option, value=option) for option in options]

    @set_attribute.autocomplete("item_name")
    @set_skill.autocomplete("item_name")
    async def owned_item_names_autocomplete(self, inter: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = itemsvc.roughly_search_item_names_by_user(current, inter.user.id)
        return [app_commands.Choice(name=option, value=option) for option in options]

    @set_attribute.autocomplete("attribute_name")
    async def attribute_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.attribute_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]

    @set_skill.autocomplete("skill_name")
    async def skill_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.skill_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]

    # @app_commands.command(name="activate", description="Activates an existing character.")
    # @app_commands.describe(charname="The character's name.")
    # async def activate_character(self, interaction: discord.Interaction, charname: str) -> None:
    #     if charactersvc.activate_character(interaction.user.id, charname):
    #         await interaction.response.send_message('Character activated.')
    #         return

    #     await interaction.response.send_message('Failed to activate character.')

    # async def show_sheet_by_name(self, interaction: discord.Interaction, character_name: str) -> None:
    #     matching_character = charactersvc.find_character_by_name(character_name)

    #     if matching_character is None:
    #         await interaction.response.send_message('Could not find a character with that name.')
    #         return

    #     await interaction.response.send_message(f"Here's the sheet for {matching_character.name}.",
    #                                             embed=self.format_sheet(interaction.user, matching_character))

    @app_commands.command(name="list", description="Display a list of all of your items.")
    @app_commands.describe(other_user="Optionally view another user's items. If ommitted, display your own items.")
    async def list_items(self, interaction: discord.Interaction, other_user: Optional[discord.Member]) -> None:
        user_id = other_user.id if other_user else interaction.user.id

        item_list = itemsvc.get_items_owned_by_user(user_id)

        if item_list is None:
            await interaction.response.send_message("There aren't any items to show!")
            return

        item_names = ', '.join(o.name for o in item_list)

    #     await interaction.response.send_message(f"Characters: {character_names}.")
