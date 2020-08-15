import discord
from discord.ext import commands
#from mcuuid.api import GetPlayerData
import requests
import time
class botcommands(commands.Cog):
    api = None
    def __init__(self, a, k):
        self.api = a
        self.apikey = k
    def get_rank(self, name):
        url = f"https://api.hypixel.net/player?key={self.apikey}&name={name}"
        res = requests.get(url)
        data = res.json()
        if data["player"] is None:
            return None
        if "prefix" in data["player"]:
            player_prefix = (data["player"]["prefix"])
            if player_prefix == "§d[PIG§b+++§d]":
                print('Rank acquired- PIG')
                return (f"[PIG+++]")
            elif player_prefix == "§c[SLOTH]":
                print('Rank acquired- Sloth')
                return ("[SLOTH]")
        if "rank" in data["player"]:
            rank = data["player"]["rank"]
            if rank == 'ADMIN':
                print('Rank acquired- Admin')
                return ('[ADMIN]')
            elif rank == 'MODERATOR':
                print('Rank acquired- Moderator')
                return ('[MOD]')
            elif rank == 'HELPER':
                print('Rank acquired- Helper')
                return ('[HELPER]')
            elif rank == 'YOUTUBER':
                print('Rank acquired- Youtube')
                return ('[YOUTUBE]')
        if "newPackageRank" in data["player"]:
            rank = (data["player"]["newPackageRank"])
            if rank == 'MVP_PLUS':
                if "monthlyPackageRank" in data["player"]:
                    mvp_plus_plus = (data["player"]["monthlyPackageRank"])
                    if mvp_plus_plus == "NONE":
                        print('Rank acquired- MVP+')
                        return ('[MVP+]')
                    else:
                        print('Rank acquired- MVP+')
                        return ("[MVP++]")
                else:
                    print('Rank acquired- MVP+')
                    return ("[MVP+]")
            elif rank == 'MVP':
                print('Rank acquired- MVP')
                return ('[MVP]')
            elif rank == 'VIP_PLUS':
                print('Rank acquired- VIP+')
                return ('VIP+')
            elif rank == 'VIP':
                print('Rank acquired- VIP')
                return ('[VIP]')
        else:
            print('Rank acquired- Non')
            return ('')
    class MyHelpCommand(commands.MinimalHelpCommand):
        def get_command_signature(self, command):
            return '{0.clean_prefix}{1.qualified_name} {1.signature}'.format(self, command)

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

    @commands.command(description="Gets info on a player.")
    async def player(self, ctx, player: str):
        player_by_username = self.api.get_player(player)
        playerstatus = player_by_username.get_status()
        embed = discord.Embed(title=f"{self.get_rank(player_by_username.get_name())} {player_by_username.get_name()}",url=f"https://plancke.io/hypixel/player/stats/{player_by_username.get_name()}")
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()
        guildid = requests.get(f"https://api.hypixel.net/guild?key={self.apikey}&player=" + uuid["id"]).json()
        if not guildid["guild"]:
            embed.add_field(name="Guild", value="No guild", inline=True)
        else:
            guild_by_id = self.api.get_guild_by_id(guildid["guild"]["_id"])
            guildname = guild_by_id.get_name()
            embed.add_field(name="Guild", value=guildname, inline=False)
            embed = discord.Embed(title=f"{self.get_rank(player_by_username.get_name())} {player_by_username.get_name()} {guildid['guild']['tag']}",url=f"https://plancke.io/hypixel/player/stats/{player_by_username.get_name()}" )

        if playerstatus["online"] == True:
            if playerstatus["mode"] == "LOBBY":
                embed.add_field(name="Status", value=f"{player_by_username.get_name()} is currently in {playerstatus['gameType']}-{playerstatus['mode']}", inline=True)
            else:
                embed.add_field(name="Status", value=f"{player_by_username.get_name()} is currently playing {playerstatus['gameType']}.", inline=True)
        elif playerstatus["online"] == False:
            embed.add_field(name="Status", value="Offline", inline=True)

        embed.add_field(name="Level", value=player_by_username.get_level(), inline=True)
        embed.add_field(name="Karma", value=player_by_username.get_karma(), inline=True)
        embed.add_field(name="Rank", value=self.get_rank(player), inline=True)
        firstlogin = requests.get(f"https://api.hypixel.net/player?key={self.apikey}&name={player}").json()
        embed.add_field(name="First Login", value=f"{time.strftime('%a, %d %b %Y', time.localtime(firstlogin['player']['firstLogin'] / 1000))}", inline=True)
        await ctx.send(embed=embed)
