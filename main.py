import discord
import os
import random
import json
import requests
from keep_alive import keep_alive

client = discord.Client()
bot_version = "v2.3.7-dev"

# ---

def showHelp():
    commands = '__The commands:__\n\n**$help** - Shows this list of commands.\n**$testbot** - Checks if the bot is online.\n**$dl <project>** - Provides the download link for the specified project. Use `$dl list` for a list of projects.\n**$stats <type>** - Provides stats for the specified media. Use `$stats list` for a list.\n**$faq <topic>** - Answers some general questions. Use `$faq list` for a list of topics.'
    return (commands)


def getUptime():
  ut_url = "https://api.uptimerobot.com/v2/getMonitors"
  ut_payload = "api_key=" + os.getenv('UPTIMEAPI') + "&format=json&logs=1"
  ut_headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache"
    }
  ut_response = requests.request("POST", ut_url, data=ut_payload, headers=ut_headers).text
  return (ut_response)


def generatePing():
    generatedping = random.randint(18, 44)
    pingstr = str(generatedping)
    return (pingstr)


# Data for $stats
def stats_getSubs():
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + os.getenv('YTCHANNEL') + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['subscriberCount'])


def stats_getVideos():
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + os.getenv('YTCHANNEL') + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['videoCount'])


def stats_getViews():
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + os.getenv('YTCHANNEL') + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['viewCount'])

# ---

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

# ---------------------------------------------------------------
# $testbot - Checks if the bot is online.
# ---------------------------------------------------------------

    if message.content.startswith('$testbot'):
        ping = generatePing()
        testbot_answer = 'Bot is online. **' + ping + 'ms**'
        await message.channel.send(testbot_answer)
        print('testbot - Answer sent')
        return

# ---------------------------------------------------------------
# $help - Shows the list of commands.
# ---------------------------------------------------------------

    if message.content.startswith('$help'):
        help = showHelp()
        await message.channel.send(help)
        print('help - Answer sent')
        return

# ---------------------------------------------------------------
# $dl - Provides the download link for the specified project.
# ---------------------------------------------------------------

    if message.content.startswith('$dl'):
        # Projects:
        dl_medieval = "**Medieval City**\nTrailer: https://youtu.be/UdZT_NrsbzQ\nWebsite: <https://theminer02.com/downloads>\nPlanetMinecraft: <https://bit.ly/3sScNG5>\nDirect: <https://bit.ly/32QA68T>"
        dl_zoo = "**TM-Zoo**\nTrailer: https://youtu.be/Beqo3e6oG9c\n*There is currently no download available*"
        dl_hytale = "**Hytale Modpack**\nVideo: https://youtu.be/oPFat5Vholk\nWebsite: <https://theminer02.com/downloads>\nDirect: <https://bit.ly/32UXoKS>"
        dl_list = "**The available projects are:**\n- Medieval City\n- TM-Zoo\n- Hytale Modpack"
        dl_unknown = "**Unknown Project**\nUse `$dl list` for a list of the projects."

        project = message.content.split("$dl ", 1)[1]

        if project == "Medieval City":
            await message.channel.send(dl_medieval)
        elif project == "TM-Zoo":
            await message.channel.send(dl_zoo)
        elif project == "Hytale Modpack":
            await message.channel.send(dl_hytale)
        elif project == "list":
            await message.channel.send(dl_list)
            print('dl - Project List sent')
            return
        else:
            await message.channel.send(dl_unknown)
            print('dl - Unknown Project sent')
            return

        print('dl - ' + project + ' sent')
        return

# ---------------------------------------------------------------
# $faq - Answers some general questions.
# ---------------------------------------------------------------

    if message.content.startswith('$faq'):
        # Topics:
        faq_invite = "**__Discord__**\n**User:** TheMiner_02#4863\n**Invite:** https://discord.gg/hrFSdAr23T"
        faq_links = "**__My social media__**\n**YouTube:** <https://youtube.com/theminer02>\n**Instagram:** <https://instagram.com/theminer_02>\n**Twitter:** <https://twitter.com/theminer_02>\n**PlanetMinecraft:** <https://planetminecraft.com/member/theminer02>\n**Website:** <https://theminer02.com/>\n**Twitch *(german)*:** <https://www.twitch.tv/theminer_02>"
        faq_bot = "**__Bot__**\n**Commands:** Use `$help`\n**General Info:** I made this bot on my own and its completely customized for me. You can't use it on your own server.\n**Version:** " + bot_version + "\n**Numbers:** ~280 lines of code, ~8 hours of work, 3 Mental Breakdowns"
        faq_donate = "**__Donate__**\nI don't know why you would want to donate something, but if you do, here you go:\n<https://streamlabs.com/theminer_02/tip>"
        faq_list = "**The available topics are:**\n- Invite\n- Links\n- Bot\n- Donate"
        faq_unknown = "**__Unknown Topic__**\nUse `$faq list` for a list of the topics."

        faq_topic = message.content.split("$faq ", 1)[1]

        if faq_topic == "Invite":
            await message.channel.send(faq_invite)
        elif faq_topic == "Links":
            await message.channel.send(faq_links)
        elif faq_topic == "Bot":
            await message.channel.send(faq_bot)
        elif faq_topic == "Donate":
            await message.channel.send(faq_donate)
        elif faq_topic == "list":
            await message.channel.send(faq_list)
            print('faq - Topic List sent')
            return
        else:
            await message.channel.send(faq_unknown)
            print('faq - Unknown Topic sent')
            return

        print('faq - ' + faq_topic + ' sent')
        return

# ---------------------------------------------------------------
# $stats - Provides stats for the specified media.
# ---------------------------------------------------------------

    if message.content.startswith('$stats'):
        # Stats:
        yt_subs = stats_getSubs()
        yt_videos = stats_getVideos()
        yt_views = stats_getViews()

        guild = message.guild

        dc_tc = str(len(guild.text_channels))
        dc_vc = str(len(guild.voice_channels))
        dc_members = str(guild.member_count + 1)
        dc_roles = str(len(guild.roles))

        # Response:
        stats_yt = "**YouTube stats**\nSubscribers: " + yt_subs + "\nTotal videos: " + yt_videos + "\nTotal views: " + yt_views + "\nChannel created: 15.09.2016"
        stats_dc = "**Discord stats**\nMembers: " + dc_members + "\nTotal text channels: " + dc_tc + "\nTotal voice channels: " + dc_vc + "\nTotal roles: " + dc_roles + "\nCreated on: 07.05.2017"
        stats_list = "**Stats are available for:**\n- YouTube\n- Discord"
        stats_unknown = "**__Unknown Type__**\nUse `$stats list` for a list of the types."

        stat_type = message.content.split("$stats ", 1)[1]

        if stat_type == "YouTube":
            await message.channel.send(stats_yt)
        elif stat_type == "Discord":
            await message.channel.send(stats_dc)
        elif stat_type == "list":
            await message.channel.send(stats_list)
            print('dl - Project List sent')
            return
        else:
            await message.channel.send(stats_unknown)
            print('stats - Unknown Type sent')
            return

        print('stats - ' + stat_type + ' sent')
        return

# ---------------------------------------------------------------
# $uptime - Displays info on the Bots uptime
# ---------------------------------------------------------------

    if message.content.startswith('$uptime'):
        # uptime = getUptime()
        await message.channel.send('This command is still in development. Try something else :)')
        print('uptime - Answer sent')
        return

# ---------------------------------------------------------------
# $ - Unknown commands
# ---------------------------------------------------------------

    if message.content.startswith('$'):
        await message.channel.send('```I dont know this command. Try $help```')
        print('Unknown Command - Answer sent')
        return


# ---------------------------------------------------------------
# Add reaction to messages that contain TM-Bot
# ---------------------------------------------------------------

    if 'TM-Bot' in message.content:
        reaction = '👀'
        await message.add_reaction(reaction)
        print('Added a reaction')
        return

keep_alive()
client.run(os.getenv('TOKEN'))
