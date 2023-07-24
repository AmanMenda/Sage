from app import config, discord, commands

class Roles(commands.Cog):
    pass

async def setup(app):
    await app.add_cog(Roles())