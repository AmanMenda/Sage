import discord
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Roles Cog ready")

    @commands.command()
    async def roles(self, ctx: commands.Context) -> None:
        self.bot.logger.info(f"roles command executed")

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload : discord.RawReactionActionEvent):
    #     guild_id = payload.guild_id
    #     channel_id = payload.channel_id
    #     message_id = payload.message_id
    #     user_id = payload.user_id
    #     emoji = payload.emoji
    #     self.bot.logger.info(f"reaction added")

    #     # Check if the reaction is from the bot
    #     if user_id == self.bot.user.id:
    #         return

    #     # Check if the reaction is added to the correct message
    #     if message_id == YOUR_MESSAGE_ID:  # Replace YOUR_MESSAGE_ID with the actual message ID
    #         guild = discord.utils.find(lambda g: g.id == guild_id, self.bot.guilds)
    #         if guild:
    #             role_name = "YOUR_ROLE_NAME"  # Replace YOUR_ROLE_NAME with the desired role name
    #             role = discord.utils.get(guild.roles, name=role_name)
    #             if role:
    #                 member = guild.get_member(user_id)
    #                 if member:
    #                     await member.add_roles(role)
    #                     self.bot.logger.info(f"Added role {role.name} to {member.name}")


async def setup(bot):
    await bot.add_cog(Roles(bot))