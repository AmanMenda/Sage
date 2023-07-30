import discord
from app import config
from utils import embeds

from discord import app_commands
from discord.ext import commands


class General(commands.Cog, name="general"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"General Cog ready")

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    async def help(self, context: commands.Context) -> None:
        prefix = config["prefix"]
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=0x9C84EF
        )
        for i in self.bot.cogs:
            cog = self.bot.get_cog(i.lower())
            if cog is not None:
                commands = cog.get_commands()
            else:
                break
            data = []
            for command in commands:
                description = command.description.partition('\n')[0]
                data.append(f"{prefix}{command.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(name=i.capitalize(),
                            value=f'```{help_text}```',
                            inline=False)
        await context.send(embed=embed)

    # @commands.hybrid_command(
    #     name="serverinfo",
    #     description="Get some useful informations about the server.",
    # )
    # async def serverinfo(self, context: commands.Context) -> None:
    #     roles = [role.name for role in context.guild.roles]

    #     if len(roles) > 50:
    #         roles = roles[:50]
    #         roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
    #     roles = ", ".join(roles)

    #     embed = discord.Embed(
    #         title="**Server Name:**",
    #         description=f"{context.guild}",
    #         color=0x9C84EF
    #     )
    #     if context.guild.icon is not None:
    #         embed.set_thumbnail(
    #             url=context.guild.icon.url
    #         )
    #     embed.add_field(
    #         name="Member Count",
    #         value=context.guild.member_count
    #     )
    #     embed.add_field(
    #         name="Text/Voice Channels",
    #         value=f"{len(context.guild.channels)}"
    #     )
    #     embed.add_field(
    #         name=f"Roles ({len(context.guild.roles)})",
    #         value=roles
    #     )
    #     embed.set_footer(
    #         text=f"Created at: {context.guild.created_at}"
    #     )
    #     await context.send(embed=embed)

    @commands.hybrid_command(
        name="invite",
        description="Get an invite link of the bot to be able to invite it.",
    )
    async def invite(self, context: commands.Context) -> None:
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discordapp.com/oauth2/authorize?&client_id={config['app_id']}&scope=bot+applications.commands&permissions={config['permissions']}).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("Please check your dms !")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.hybrid_command(
        name="server",
        description="Generate an invite link to join our server.",
    )
    async def send_server_link(self, context: commands.Context) -> None:
        embed = discord.Embed(
            description=f"Join the support server of the bot by clicking [here](https://discord.gg/RpyEAqFvQ9).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("The link has been sent in your dms !")
        except discord.Forbidden:
            await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))