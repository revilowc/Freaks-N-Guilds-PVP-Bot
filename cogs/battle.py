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

dbhost = os.getenv('dbhost')
dbuser = os.getenv('dbuser')
dbpass = os.getenv('dbpass')
dbname = os.getenv('dbname')
dbport = int(os.getenv('dbport'))

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
    port=dbport,
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

        mycursor.execute("INSERT INTO Users (userID, gold, freak, hunted, hd, sb, o, ss, ih, pa, rn, ma, eh, vv, d ,t) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
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

    @discord.ui.button(label='Close Armoury', style=discord.ButtonStyle.green)
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


# class BattleDropdown(discord.ui.Select):
#     def __init__(self):
#
#         options = [
#             discord.SelectOption(label=self.view.attacklowname,
#                                  description="+10 Attack Damage for High Attack"),
#         ]
#
#         super().__init__(placeholder='Please select an item to equip...',
#                          min_values=1, max_values=1, options=options)
#
#     async def callback(self, interaction: discord.Interaction):
#         if interaction.user != self.view.ctx.author:
#             await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.view.ctx.author.mention}. Use your own commands!**", color=embedcolor), ephemeral=True)
#             return
#
#         if self.values[0] == 'Hidden Dagger':
#
#
# class BattleDropDownView(discord.ui.View):
#     def __init__(self, ctx, equipment):
#         super().__init__()
#         self.ctx = ctx
#         self.equipment = equipment
#
#         self.add_item(EquipDropdown())
#
#     async def on_timeout(self):
#         if self.msg:
#             await self.msg.edit(embed=discord.Embed(description="**Timed out... Cancelled battle!**", color=embedcolor), view=None)
#
#
# class ConfirmBattle(discord.ui.View):
#     def __init__(self, ctx, opponent):
#         super().__init__()
#         self.ctx = ctx
#         self.opponent = opponent
#         self.msg = None
#
#     @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
#     async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
#         if interaction.user != self.opponent:
#             await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.opponent.mention}!**", color=embedcolor), ephemeral=True)
#             return
#
#         self.clear_items()
#         self.stop()
#
#         await self.msg.edit(view=self)
#
#         mycursor.execute("SELECT freak, equipment1, equipment2, equipment3 FROM Users WHERE userID=%(userID)s OR userID=%(userID2)s",
#                          {'userID': self.ctx.author.id, 'userID2': opponent.id})
#
#         for x in mycursor:
#
#             embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats", color=embedcolor)
#             embed.set_footer(text=footertext, icon_url=ctx.guild.icon.url)
#             embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
#             embed.timestamp = discord.utils.utcnow()
#
#             lowaccuracy = baseattacklowaccuracy
#             highaccuracy = baseattackhighaccuracy
#
#             if x[0] == "V":
#                 freakname = "Vampire"
#                 buff1 = "+10 Accuracy"
#                 buff2 = "+15 Attack Damage"
#                 health = vampirebasehealth
#                 defense = vampirebasedefense
#                 buff1name = vampirebuff1name
#                 buff2name = vampirebuff2name
#                 attacklow = vampirebaseattacklow
#                 attackhigh = vampirebaseattackhigh
#                 attacklowname = vampireattacklowname
#                 attackhighname = vampireattackhighname
#
#             elif x[0] == "W":
#                 freakname = "Werewolf"
#                 buff1 = "+10 Accuracy"
#                 buff2 = "+10 Defense"
#                 health = werewolfbasehealth
#                 defense = werewolfbasedefense
#                 buff1name = werewolfbuff1name
#                 buff2name = werewolfbuff2name
#                 attacklow = werewolfbaseattacklow
#                 attackhigh = werewolfbaseattackhigh
#                 attacklowname = werewolfattacklowname
#                 attackhighname = werewolfattackhighname
#
#             elif x[0] == "S":
#                 freakname = "Skeleton"
#                 buff1 = "+15 Attack Damage"
#                 buff2 = "+10 Defense"
#                 health = skeletonbasehealth
#                 defense = skeletonbasedefense
#                 buff1name = skeletonbuff1name
#                 buff2name = skeletonbuff2name
#                 attacklow = skeletonbaseattacklow
#                 attackhigh = skeletonbaseattackhigh
#                 attacklowname = skeletonattacklowname
#                 attackhighname = skeletonattackhighname
#
#         await interaction.response.send_message(embed=embed, view=view)
#
#     @discord.ui.button(label='No', style=discord.ButtonStyle.red)
#     async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
#         if interaction.user != self.opponent:
#             await interaction.response.send_message(embed=discord.Embed(description=f"**You are not {self.opponent.mention}!**", color=embedcolor), ephemeral=True)
#             return
#
#         self.clear_items()
#         self.stop()
#
#         await self.msg.edit(view=self)
#
#         await interaction.response.send_message(f"{self.ctx.author.mention}{self.opponent.mention}", embed=discord.Embed(description="**Cancelled battle!**", color=embedcolor))
#
#     async def on_timeout(self):
#         if self.msg:
#             await self.msg.edit(embed=discord.Embed(description="**Timed out... Cancelled battle!**", color=embedcolor), view=None)


class Battle(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.persistent_views_added = False

    # Commands
    # @slash_command(guild_ids=guildIDs, description="Battle with your Freak")
    # async def battle(self, ctx, opponent: discord.Member):
    #     mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
    #                      'userID': ctx.author.id})
    #     for x in mycursor:
    #         if x[0] == 0:
    #             await ctx.respond(embed=discord.Embed(description=f"**You don't have a Freak! Type `/pickfreak <freak>` to pick your own Freak.**", color=embedcolor), ephemeral=True)
    #             return
    #
    #     mycursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %(userID)s LIMIT 1)", {
    #                      'userID': opponent.id})
    #     for x in mycursor:
    #         if x[0] == 0:
    #             await ctx.respond(embed=discord.Embed(description=f"**{opponent.mention} doesn't have a Freak!**", color=embedcolor), ephemeral=True)
    #             return
    #
    #     view = ConfirmBattle(ctx, opponent)
    #
    #     await ctx.respond(f"{ctx.author.mention}{opponent.mention}", embed=discord.Embed(description=f"**{opponent.mention}, you have been challenged to a battle by {ctx.author.mention}! Do you accept?**", color=embedcolor), view=view)
    #
    #     view.msg = await ctx.interaction.original_message()

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
        if not self.persistent_views_added:
            # self.client.add_view(UFOView(self.client))
            self.persistent_views_added = True

    @tasks.loop(hours=12.0)
    async def resethunt(self):
        mycursor.execute("UPDATE Users SET hunted = False")
        mydb.commit()


def setup(client):
    client.add_cog(Battle(client))
