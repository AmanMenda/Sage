import discord
from utils import embeds

from discord.ext import commands
from app import db

cursor = db.cursor()

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Level Cog ready")

    @commands.command(help="Use this command to display your current level")
    async def level(self, ctx: commands.Context) -> None:

        # fetch the required data
        cursor.execute("SELECT Level, Xp FROM levels WHERE UserId = ?", (str(ctx.author.id),))
        result = cursor.fetchone()
        # delete request
        await ctx.message.delete()
        embed = embeds.current_level(author=ctx.author, bot_latency=self.bot.latency, lvl=result[0], xp=result[1])
        self.bot.logger.info(f"level command executed")
        return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Level(bot))