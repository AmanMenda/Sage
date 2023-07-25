import sys, os

import discord
from discord.ext import commands, tasks

import random
import json
import platform
import asyncio
import sqlite3

import logger

EXTENSIONS = [
    "cogs.roles",
    "cogs.level",
]

#define your roles from the less important one to the most important one
activity_roles = ["Explorateur", "Fabricant d'idées", "Créateur émergent",
             "Maître de la collaboration", "Pionnier des univers virtuels",
             "Contributeur émérite", "Pilier de la communauté"]

def levels(activity_roles: list[str]) -> dict:
    '''
    A function to automatically define levels,
    their corresponding XPs and roles.
    Should the levels be defined in the db or in the code ?
    '''
    XPs = 0
    levels = {}
    roles_idx = 0

    for i in range(1, 301, +1):
        if i % 20 == 0 or i == 1: # est un palier
            levels[i] = {XPs: activity_roles[roles_idx]}
            if roles_idx != len(activity_roles) - 1:
                roles_idx += 1
        else:
            levels[i] = {XPs: ""}

        if i <= 100:
            XPs += 10
        else:
            XPs += 5

    return levels



# add a close function to close the opened connection






def load_config(filepath: str):
    '''
    Check if the specified filepath exist and load its content
    '''
    if not os.path.isfile(filepath):
        sys.exit(f"{filepath} not found, please provide a {filepath} and try again.")
    else:
        with open(filepath) as file:
            return json.load(file)

config = load_config("config.json")
intents = discord.Intents.default()
intents.members = True  # Subscribe to the privileged members intent
intents.reactions = True  # Enable reaction events
intents.message_content = True

db = sqlite3.connect('src/database/level.db')
cursor = db.cursor()

class App(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config["prefix"],
                        intents=intents) # missing a help command
        self.logger = logger.create(name="discord_bot", logfilename="discord.log")
        self.level_dict = levels(activity_roles)

    async def on_ready(self):
        '''
        Print general infos about the bot and the platform its running on.
        '''
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")
        self.status_task.start() # start status loop task
        cursor.execute("CREATE TABLE IF NOT EXISTS levels (UserId VARCHAR(30), Level INTEGER, Xp BIGINT, ServerId VARCHAR(30))")
        db.commit()

    async def on_message(self, message: discord.Message) -> None:
        '''
        Process every messages sent by users and trigger the appropriate
        command.
        '''
        if message.author == self.user or message.author.bot:
            return
        # Ajouter 1/2 XP à celui qui l'a envoyé. Si Xp == Level[actuel + 1], update user level in database,
        # reset XPs, assign new role and remove last role
        message_author_id = message.author.id
        cursor.execute("SELECT Level, Xp FROM levels WHERE UserId = ?", (str(message_author_id),)) # do not change this,
                                                                                            # the second value should be a tuple
        result = cursor.fetchone()
        # result format should be -> [(Level: int, Xp: bigint)]
        current_level, current_xp = result[0]

        # Par défaut, incrémenter
        current_xp += 0.5

        # Vérifier si chaine de caractère associée à xps du niveau était vide ou non.
        if (current_level <= 100 and current_xp == (self.level_dict[current_level + 1].keys()[0])) or \
            (current_level > 100 and current_xp == (self.level_dict[current_level + 1].keys()[0])):

            old_role_name = (self.level_dict[current_level])[current_xp]
            current_level += 1


            if (self.level_dict[current_level])[current_xp] != "":
                new_role_name = (self.level_dict[current_level])[current_xp]
                message.author.remove_role(old_role_name)
                message.author.add_roles(new_role_name)
            current_xp = 0

        # update current_xp and current_level in database
        cursor.execute("UPDATE levels SET Level = ?, Xp = ? WHERE UserId = ?", current_level, current_xp, str(message_author_id))
        db.commit()
        await self.process_commands(message)


    async def on_member_join(self, member: discord.Member):
        '''
        Connect to the SQL database and create a row of the new member in the table 'levels'.
        '''
        cursor.execute("INSERT INTO levels VALUES (?, ?, ?, ?)",
                    str(member.id), 1, 0, config["server_id"])
        db.commit()

    async def on_command_completion(self, context: commands.Context) -> None:
        """
        The code in this event is executed every time a normal command has been *successfully* executed.

        :param context: The context of the command that has been executed.
        """
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])
        if context.guild is not None:
            self.logger.info(
                f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})"
            )
        else:
            self.logger.info(
                f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs"
            )

    async def on_command_error(self, context: commands.Context, error) -> None:
        """
        The code in this event is executed every time a normal valid command catches an error.

        :param context: The context of the normal command that failed executing.
        :param error: The error that has been faced.
        """
        if isinstance(error, commands.CommandNotFound):
            self.logger.warning(
                f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})"
            )
        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
                color=0xE02B2B,
            )
            await context.send(embed=embed)
        else:
            raise error

    @tasks.loop(seconds=20)
    async def status_task(self) -> None:
        """
        Setup the game status task of the bot.
        """
        statuses = ["avec toi!", "avec Krypton!", "avec les humains!"]
        await self.change_presence(activity=discord.Game(random.choice(statuses)))


    def run(self):
        super().run(config['token'], reconnect=True)

async def load_cogs(app):
    for extension in EXTENSIONS:
        try:
           await app.load_extension(extension)
        except Exception as e:
            sys.stderr.write(f'{type(e).__name__}: {e}\n')
            sys.exit(-1)

def main():
    app = App()
    asyncio.run(load_cogs(app))
    app.run()

if __name__ == '__main__':
    main()