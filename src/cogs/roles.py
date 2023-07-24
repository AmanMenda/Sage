from discord.ext import commands

class Roles(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("roles ready")
        pass

    @commands.command()
    async def roles(self, ctx: commands.Context) -> None:
        print("roles")
        pass

async def setup(bot):
    await bot.add_cog(Roles(bot))