from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.logger.info(f"Level Cog ready")

    @commands.command()
    async def level(self, ctx: commands.Context) -> None:
        self.bot.logger.info(f"level command executed")

async def setup(bot):
    await bot.add_cog(Level(bot))