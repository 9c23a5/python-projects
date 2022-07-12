from datetime import datetime
import discord
import json

with open('settings.json') as configfile:
    settings = json.load(configfile)

token = settings['token']
usersToSpy = settings['userstospy']
channelid = settings['channel']
admin = settings['admin']

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def build_activity(self, activities):
        activityString = []
        for activity in activities:
            if activity.type == discord.ActivityType.listening:
                activityString.append("Listening to {0} - {1}".format(activity.artist, activity.title))
            elif activity.type == discord.ActivityType.playing:
                if activity.details != None and activity.state == None:
                    activityString.append("Playing {0} ({1})".format(activity.name, activity.details))
                elif activity.details != None and activity.state != None:
                    activityString.append("Playing {0} ({1} - {2})".format(activity.name, activity.details, activity.state))
                else:
                    activityString.append("Playing {0}".format(activity.name))
        if len(activityString) == 0:
            return ["None"]
        else:
            return activityString

    async def on_member_update(self, before, after):
        if before.id in usersToSpy and before.activities != after.activities:
            channel = self.get_channel(channelid)
            time = datetime.now().strftime("%H:%M:%S")
            if before.status != after.status:
                await channel.send("[{0}] {1}#{2} changed status from {3} to {4}".format(time, after.name, after.discriminator, before.status, after.status))
            else:
                embed = discord.Embed(title=f"Changed activity [{time}]")
                embed.add_field(name='User', value=before.mention)
                beforeActivities = await self.build_activity(before.activities)
                afterActivities = await self.build_activity(after.activities)

                # Debugging
                # print("Before: {0}".format('\n'.join(beforeActivities)))
                # print("After: {0}".format('\n'.join(afterActivities)))
                
                embed.add_field(name='Before', value="\n".join(beforeActivities))
                embed.add_field(name='After', value="\n".join(afterActivities))
                await channel.send(embed=embed)


intents = discord.Intents.default()
intents.members=True
intents.presences=True

client = MyClient(intents=intents)
client.run(token)
