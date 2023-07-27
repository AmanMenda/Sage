from discord.ext import commands
import discord

# define an object Embed which goal is to generate all kinds of embed

def current_level(author: discord.Member, bot_latency : float, lvl: int, xp : float):
    embed = discord.Embed(
        title='Vous avez demandé à connaître votre niveau ?',
        color=0x34495E, # define the side-bar color as navy
        description="Voici la réponse à votre requête :)"
    )

    embed.add_field(name="Auteur de la commande", value=f"{author.mention}", inline=True)
    embed.add_field(name="Niveau actuel", value=f"{lvl}", inline=True)
    embed.add_field(name="Points d'expérience", value=f"{xp} pts", inline=True)

    embed.set_image(url="https://i.pinimg.com/originals/e4/15/c4/e415c48c6387706cc02f92b09501cab5.gif")
    embed.set_footer(text="Ping: {:.2f}".format(bot_latency * 1000) + " ms")
    return (embed)


def level_up(author: discord.Member, bot_latency : float, lvl: int):
    embed = discord.Embed(
        title=f'🎉 Bravo! 🎉 Tu as atteint le niveau {lvl}.',
        color=0x34495E, # define the side-bar color as navy
        description=f"{author.mention} Continue comme ça, tu progresses à une vitesse incroyable ! 🚀💪"
    )
    embed.set_footer(text="Ping: {:.2f}".format(bot_latency * 1000) + " ms")
    return (embed)

def role_upgrade(author: discord.Member, bot_latency : float, lvl: int, xp: float, role: discord.Role):
    
    embed = discord.Embed(
        title=f'🌟 Félicitations ! 🌟 Nous sommes extrêmement fiers de tes progrès et de ton engagement dans notre communauté.',
        color=0x34495E, # define the side-bar color as navy
        description=f"{author.mention} Continue à participer activement, tu es une véritable source d'inspiration pour tous ! 🎉🥳"
    )

    embed.add_field(name="Nouveau grade", value=f"{role}", inline=True)
    embed.add_field(name="Niveau actuel", value=f"{lvl}", inline=True)
    embed.set_image(url="https://media.giphy.com/media/tEcIyVc6ukQV2eb86t/giphy.gif")
    embed.set_footer(text="Ping: {:.2f}".format(bot_latency * 1000) + " ms")
    return (embed)