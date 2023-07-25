import discord
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

        # generate a custom answer
        embed = discord.Embed(
            title='Vous avez demandé à connaître votre niveau ?',
            color=0x34495E, # define the side-bar color as navy
            description="Voici la réponse à votre requête :)"
        )

        embed.add_field(name="Auteur de la commande", value=f"{ctx.author.mention}", inline=True)
        embed.add_field(name="Niveau actuel", value=f"{result[0]}", inline=True)
        embed.add_field(name="Points d'expérience", value=f"{result[1]} pts", inline=True)

        embed.set_image(url="https://i.pinimg.com/originals/e4/15/c4/e415c48c6387706cc02f92b09501cab5.gif")
        embed.set_footer(text="Ping: {:.2f}".format(self.bot.latency * 1000) + " ms")
        self.bot.logger.info(f"level command executed")
        return await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Level(bot))