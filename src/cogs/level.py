from discord.ext import commands
from app import db

cursor = db.cursor()

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Level Cog ready")

    @commands.command()
    async def level(self, ctx: commands.Context) -> None:
        result = cursor.execute("SELECT Level FROM levels WHERE UserId = ?", ctx.author.id)
        embed = discord.Embed(
            title='level',
            color=0xE02B2B,
            description=f"Vous êtes actuellement au niveau {result[0]}"
        )
        self.bot.logger.info(f"level command executed")

async def setup(bot):
    await bot.add_cog(Level(bot))