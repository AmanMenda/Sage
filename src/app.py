import sys, os

import discord
from discord.ext import commands

import json

import platform

import asyncio

EXTENSIONS = [
    "cogs.roles",
    "cogs.level",
]

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
intents.message_content = True

class App(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config["token"],
                        intents=intents) # missing a help command

    async def on_ready(self):
        '''
        Print general infos about the bot and the platform its running on.
        '''
        print(f"Logged in as {self.user.name}")
        print(f"discord.py API version: {discord.__version__}")
        print(f"Python version: {platform.python_version()}")
        print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
        print("-------------------")

    async def on_message(self, message: discord.Message) -> None:
        '''
        Process every messages sent by users and trigger the appropriate
        command.
        '''
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

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