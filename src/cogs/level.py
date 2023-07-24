from app import config, discord, commands

class level(commands.Cog):
    pass

async def setup(app):
    await app.add_cog(level())