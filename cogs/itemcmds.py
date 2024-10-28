from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from services import itemsvc
from util.errors import ItemException, PermissionException, StatException
import models

async def setup(bot):
    await bot.add_cog(ItemCog(bot))

class ItemCog(commands.GroupCog, name='item', description='Item commands'):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="create", description="Creates a new item.")
    @app_commands.describe(itemname="The items's name.")
    async def create_item(self, interaction: discord.Interaction, itemname: str) -> None:
        itemsvc.create_item(interaction.user.id, itemname)
        await interaction.response.send_message('Item created.')

    @app_commands.command(name="details", description="Display details about an item.")
    @app_commands.describe(item_name="Find an item using its name.")
    async def show_details(self,interaction: discord.Interaction, item_name: str) -> None:
        matching_item = itemsvc.find_item_by_name(item_name)

        if matching_item is None:
            await interaction.response.send_message('Could not find a item with that name.')
            return
        
        result = ''
        effects = matching_item.get_effects()
        for effect in effects:
            result += f'{effect}: {effects[effect]}'

        await interaction.response.send_message(f"Here's the details for {matching_item.name}: {result}")

    @app_commands.command(name="list", description="Display a list of all of your items.")
    @app_commands.describe(other_user="Optionally view another user's items. If ommitted, display your own items.")
    async def list_items(self, interaction: discord.Interaction, other_user: Optional[discord.Member]) -> None:
        user_id = other_user.id if other_user else interaction.user.id

        item_list = itemsvc.get_items_owned_by_user(user_id)

        if item_list is None:
            await interaction.response.send_message("There aren't any items to show!")
            return

        item_names = ', '.join(o.name for o in item_list)

        await interaction.response.send_message(f"Items: {item_names}.")

    @app_commands.command(name="setattribute", description="Adds an effect to one of your items.")
    @app_commands.describe(attribute_name="The name of the attribute to edit.", value="An integer to set the attribute's value to.")
    async def set_attribute(self, interaction: discord.Interaction, attribute_name: str, value: int) -> None:
        try:
            itemsvc.set_attribute(interaction.user.id, attribute_name, value)
            await interaction.response.send_message("Attribute successfully set.")
        except (ItemException, PermissionException, StatException) as e:
            await interaction.response.send_message(f"An error occurred while setting the attribute: {e}")

    @app_commands.command(name="setskill", description="Set the value of one of your character's skills.")
    @app_commands.describe(skill_name="The name of the skill to edit.", value="An integer to set the skill's value to.")
    async def set_skill(self, interaction: discord.Interaction, skill_name: str, value: int) -> None:
        try:
            itemsvc.set_skill(interaction.user.id, skill_name, value)
            await interaction.response.send_message("Skill successfully set.")
        except (ItemException, PermissionException, StatException) as e:
            await interaction.response.send_message(f"An error occurred while setting the skill: {e}")

    @set_attribute.autocomplete("attribute_name")
    async def attribute_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.attribute_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]

    @set_skill.autocomplete("skill_name")
    async def skill_name_autocomplete(self, _: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        options = models.stats.skill_pretty_names.values()
        return [app_commands.Choice(name=option, value=option) for option in options if option.casefold().startswith(current.casefold())][:25]
