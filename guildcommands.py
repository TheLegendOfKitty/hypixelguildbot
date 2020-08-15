import discord
from discord.ext import commands
#from mcuuid.api import GetPlayerData
import requests
class botcommands(commands.Cog):
    api = None
    def __init__(self, a):
        self.api = a


    @commands.command(description="Get basic information on a guild.")
    async def exp(self, ctx, exprequirment: int, *, guildname: str):
        await ctx.send("Checking for members under " + str(exprequirment) + " gexp in " + guildname + "!")
        guild_by_name = self.api.get_guild_by_name(guildname)
        rawguildjson = guild_by_name.get_raw_guild()
        memberdict = {}
        membersbelowrequirment = {}
        embed = discord.Embed(title="Weekly Exp Count for " + guildname)
        for i in range(0, len(rawguildjson["members"])):
            memberdict[rawguildjson["members"][i]["uuid"]] = 0

            for item in rawguildjson["members"][i]["expHistory"]:
                memberdict[rawguildjson["members"][i]["uuid"]] += int(rawguildjson["members"][i]["expHistory"][item])

            if memberdict[rawguildjson["members"][i]["uuid"]] < exprequirment:
                data = requests.get("https://sessionserver.mojang.com/session/minecraft/profile/" + rawguildjson["members"][i]["uuid"]).json()
                membersbelowrequirment[data["name"]] = int(memberdict[rawguildjson["members"][i]["uuid"]])
                embed.add_field(name=data["name"], value=membersbelowrequirment[data["name"]], inline=True)
        embed.set_footer(text="Made by CatsRCool#2238 <3")
        await ctx.send(embed=embed)
        #print(rawguildjson["guild"]["members"]["expHistory"])
        #print(rawguildjson["members"][0]["expHistory"])
        #await ctx.send(memberdict)
        #print(memberdict)
        #print(membersbelowrequirment)

    class MyHelpCommand(commands.MinimalHelpCommand):
        def get_command_signature(self, command):
            return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)
