from discord.ext import commands

class Level(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("ready")
        pass

    @commands.command()
    async def level(self, ctx: commands.Context) -> None:
        print("rlevel")
        pass

async def setup(bot):
    await bot.add_cog(Level(bot))