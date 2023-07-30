from app import load_config

import discord
from discord.ext import commands

colors = load_config("colors.json")
urls = load_config("assets.json")

def current_level(author: discord.Member, bot_latency : float, lvl: int, xp : float, next_rq : float):
    embed = discord.Embed(
        title='Vous avez demandé à connaître votre niveau ?',
        color=0x34495E, # define the side-bar color as navy
        description="Voici la réponse à votre requête :)"
    )

    embed.add_field(name="Auteur de la commande", value=f"{author.mention}", inline=True)
    embed.add_field(name="Niveau actuel", value=f"{lvl}", inline=True)
    embed.add_field(name="Points d'expérience", value=f"{xp} / {next_rq} pts ", inline=True)

    embed.set_image(url=urls["whale animation"])
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
        title=f'🌟 Félicitations ! 🌟 Nous te remercions pour ta participation au sein de notre communauté.',
        color=0x34495E, # define the side-bar color as navy
        description=f"{author.mention} Continue à participer activement pour plus d'accès au sein de la communauté, tu es une véritable source d'inspiration pour tous ! 🎉🥳"
    )

    embed.add_field(name="Nouveau grade", value=f"{role}", inline=True)
    embed.add_field(name="Niveau actuel", value=f"{lvl}", inline=True)
    embed.set_image(url=urls["rengoku animation"])
    embed.set_footer(text="Ping: {:.2f}".format(bot_latency * 1000) + " ms")
    return (embed)