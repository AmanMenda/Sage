import discord
from utils import embeds

from discord.ext import commands
from app import db, activity_roles, levels

cursor = db.cursor()

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.level_dict = levels(activity_roles)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Level Cog ready")

    @commands.command(help="Use this command to display your current level")
    async def level(self, ctx: commands.Context) -> None:

        # fetch the required data
        cursor.execute("SELECT Level, Xp FROM levels WHERE UserId = ?", (str(ctx.author.id),))
        result = cursor.fetchone()
        next_level_requirement = (self.level_dict[result[0] + 1])[0]
        # delete request
        await ctx.message.delete()
        embed = embeds.current_level(author=ctx.author, bot_latency=self.bot.latency, lvl=result[0], xp=result[1], next_rq=next_level_requirement)
        self.bot.logger.info(f"level command executed")
        return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Level(bot))