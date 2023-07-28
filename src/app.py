import sys, os

import discord
from discord.ext import commands, tasks

from typing import List
import json
import random
import asyncio
import sqlite3
import platform

import utils
import logger

EXTENSIONS = [
    "cogs.level",
]

#define your roles from the less important one to the most important one
activity_roles = ["Explorateur", "Fabricant d'idées", "Créateur émergent",
             "Maître de la collaboration", "Pionnier des univers virtuels",
             "Contributeur émérite", "Pilier de la communauté"]

def levels(acty_roles: List[str]) -> dict:
    '''
    A function to automatically define levels,
    their corresponding XPs and roles.
    This one define from level 0 to 300 and the ultimate level will
    soon be taken as a parameter
    '''
    XPs = 0
    levels = {}
    roles_idx = 0

    for i in range(0, 301, +1):
        if i % 20 == 0 and i != 0:
            if roles_idx != len(acty_roles) - 1:
                roles_idx += 1
            levels[i] = (XPs, acty_roles[roles_idx])
        else:
            levels[i] = (XPs, acty_roles[roles_idx])

        XPs += 10 if i <= 100 else 5

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
intents.guilds = True
intents.members = True  # Subscribe to the privileged members intent
intents.reactions = True  # Enable reaction events
intents.message_content = True

db = sqlite3.connect('src/database/level.db')
cursor = db.cursor()

class App(commands.Bot):
    def __init__(self):
        global activity_roles
        super().__init__(command_prefix=config["prefix"],
                        intents=intents) # missing a help command
        self.logger = logger.create(name="discord_bot", logfilename="discord.log")
        self.level_dict = levels(activity_roles)
        # print(json.dumps(self.level_dict))

    async def on_ready(self):
        '''
        Print general infos about the bot and the platform its running on
        and create a database to store level, xp of a user on a server
        '''
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"discord.py API version: {discord.__version__}")
        self.logger.info(f"Python version: {platform.python_version()}")
        self.logger.info(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        self.logger.info("-------------------")
        self.status_task.start() # start status loop task
        cursor.execute("CREATE TABLE IF NOT EXISTS levels (UserId VARCHAR(30), Level INTEGER, Xp FLOAT, ServerId VARCHAR(30))")
        db.commit()

    async def on_message(self, message: discord.Message) -> None:
        '''
        Process every messages sent by users and trigger the appropriate
        command. This function also serves the purpose of adding experience
        points to the message author, grant him new roles according to his level
        to maximise his interactions in the server.
        '''
        if message.author == self.user or message.author.bot:
            return

        # fetch the data from the database
        message_author_id = message.author.id
        cursor.execute("SELECT Level, Xp FROM levels WHERE UserId = ?", (str(message_author_id),)) # do not change this, the second value should be a tuple
        db.commit()
        result = cursor.fetchone() # result format should be -> [Level: int, Xp: float]

        self.logger.debug(f"level: {result[0]}, xps: {result[1]}")
        current_level = result[0]
        current_xp = result[1]

        # By default, increment xp value
        current_xp += len(message.content) / 4

        next_level_xp_requirement = (self.level_dict[current_level + 1])[0]
        self.logger.debug(f"next_level_xp_requirement: {next_level_xp_requirement}")
        if current_xp >= next_level_xp_requirement:
            old_role_name = (self.level_dict[current_level])[1]
            current_level += 1
            new_role_name = (self.level_dict[current_level])[1]
            current_xp -= next_level_xp_requirement
            self.logger.info(f"=>> Level up! {current_level - 1} = > {current_level}")
            if new_role_name != old_role_name:
                old_role = discord.utils.get(message.guild.roles, name=old_role_name)
                new_role = discord.utils.get(message.guild.roles, name=new_role_name)
                if (new_role and old_role):
                    # remove old role
                    await message.author.remove_roles(old_role)
                    # add new role
                    await message.author.add_roles(new_role)
                    self.logger.info(f"Level up! new role assigned: new_role={new_role_name}")
                    embed = utils.embeds.role_upgrade(author=message.author, bot_latency=self.latency, lvl=current_level, role=new_role)
            else:
                embed = utils.embeds.level_up(author=message.author, bot_latency=self.latency, lvl=current_level)
            await message.channel.send(embed=embed)

        # update current_xp and current_level in database
        self.logger.debug(f"Message author id: {str(message_author_id)}")
        cursor.execute("UPDATE levels SET Level = ?, Xp = ? WHERE UserId = ?", (current_level, current_xp, str(message_author_id)))
        db.commit()

        await self.process_commands(message)

    async def on_member_join(self, member: discord.Member):
        '''
        Connect to the SQL database and create a row of the new member in the table 'levels'.
        TODO: By default, the first role of the list is assigned to new members.
        '''
        default_role = discord.utils.get(member.guild.roles, name=activity_roles[0])
        await member.add_roles(default_role)        
        cursor.execute("INSERT INTO levels VALUES (?, ?, ?, ?)",
                    str(member.id), 1, 0, config["server_id"]) # not tested yet, may need data to be packed or use executemany
        db.commit()

    async def on_command_completion(self, context: commands.Context) -> None:
        '''
        The code in this event is executed every time a normal command has been *successfully* executed.
        '''
        full_command_name = context.command.qualified_name
        split = full_command_name.split(" ")
        executed_command = str(split[0])

        if context.guild is not None:
            self.logger.info(f"Executed {executed_command} command in {context.guild.name} (ID: {context.guild.id}) by {context.author} (ID: {context.author.id})")
        else:
            self.logger.info(f"Executed {executed_command} command by {context.author} (ID: {context.author.id}) in DMs")

    async def on_command_error(self, context: commands.Context, error) -> None:
        '''
        The code in this event is executed every time a normal valid command catches an error.
        '''
        if isinstance(error, commands.CommandNotFound):
            self.logger.warning(f"Command not found: {context.message.content} by {context.author} (ID: {context.author.id})")

        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            hours = hours % 24
            embed = discord.Embed(
                description=f"**Please slow down** - You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
                color=0x5865F2,
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="You are missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to execute this command!",
                color=0x5865F2,
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description="I am missing the permission(s) `"
                + ", ".join(error.missing_permissions)
                + "` to fully perform this command!",
                color=0x5865F2,
            )
            await context.send(embed=embed)

        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="Error!",
                # We need to capitalize because the command arguments have no capital letter in the code.
                description=str(error).capitalize(),
                color=0x5865F2,
            )
            await context.send(embed=embed)

        else:
            raise error

    @tasks.loop(seconds=120)
    async def status_task(self) -> None:
        '''
        Setup the game status task of the bot.
        '''
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