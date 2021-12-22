import discord
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import random

client = commands.Bot(command_prefix='?', help_command=None)
client.remove_command('help')

@client.command()
async def help(ctx, args=None):
    help_embed = discord.Embed(title='This is help command.', color=5814783)
    command_names_list = [x.name for x in client.commands]
    if not args:
        help_embed.set_author(name='DiscordMaid', icon_url='https://static.wikia.nocookie.net/iyapan/images/2/22/Chitose_Itou.png')
        help_embed.add_field(name='`Administrator:` ', value='?kick @user\n?banned @user\n?unban <name#1234>\n?mute @user\n?unmute @user', inline=False)
        help_embed.add_field(name='`Anime:`', value='?anime <anime name>\n?chara <character name> \n?randomhentai (send random hentai pics)', inline=False)
        help_embed.add_field(name='`Other:`', value='?wiki <keyword> (wiki search)\n?katagaul <kata> (arti kata gaul, INDONESIA ONLY)\n?revip <ip> (reverse ip to domain)', inline=False)
        help_embed.set_image(url='https://static.wikia.nocookie.net/iyapan/images/2/22/Chitose_Itou.png')
    elif args in command_names_list:
        help_embed.add_field(name=args, value=client.get_command(args).help)
    else:
        pass

    await ctx.send(embed=help_embed)

# favorite anime checker
# favorite character checker

hentai = [
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Itsuki-Nakano-The-Quintessential-Quintuplets-rule34-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Mai-Sakurajima-Rascal-Does-Not-Dream-of-Bunny-Girl-Senpai-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Elinalise-Dragonroad-Mushoku-Tensei-rule34-uncensored-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Raiden-Shogun-Genshin-Impact-animated-2d-hentai-video.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Mieruko-chan-Miko-Yotsuya-rule34-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Naruto-Shizune-hentai-uncensored-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/12/Siesta-The-Detective-Is-Already-Dead-pussy-creampied-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Hanabi-Hyuuga-Naruto-hentai-wet-pussy-fucked-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Darling-in-the-FranXX-Zero-Two-rule34-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Genshin-Impact-uncensored-Hu-Tao-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Emilia-Re-Life-in-a-Different-World-from-Zero-footjob-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Utaha-Kasumigaoka-Saekano-Flat-2d-hentai-video.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Genshin-Impact-Sara-Kujou-rule-34-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Miss-Kobayashis-Dragon-Maid-Tohru-footjob-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/11/Black-Clover-Noelle-Silva-pussy-and-ass-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Hu-Tao-Pussy-and-feet-Genshin-Impact-2d-rule34-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Ayaka-Kamisato-Genshin-Impact-pussy-creampie-hentai-image.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Genshin-Impact-Miko-Yae-and-Raiden-Shogun-1.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Ganyu-Genshin-Impact-gangbang-and-creampie.webp',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Komi-Cant-Communicate-Shouko-Komi-2d-hentai-552x781.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Hinata-Hyuga-pussy-fucked-POV-Naruto-2D-hentai-image-552x833.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Ayumu-Uehara-and-Yuu-Takasaki-Love-Live-hentai-552x761.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Baal-Genshin-Impact-Raiden-Shogun-2d-hentai-art-552x690.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/10/Genshin-Impact-Hu-Tao-2d-hentai-porrn-552x390.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/09/Kurumi-Tokisaki-2d-hentai-Date-A-Live-552x779.jpg',
    'https://cdn.2dhentai.club/wp-content/uploads/2021/09/Ayaka-Kamisato-Genshin-Impact-2d-hentai-creampie-552x784.jpg',
]

memes = [
    ''
]

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='?help'))
    print('We have logged in as {0.user}'.format(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return

@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    embed = discord.Embed(title='Kick!', description='{} Has Been Kicked!'.format(member), color=15548997)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def banned(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    embed = discord.Embed(title='Banned!', description='{} Has Been Banned!'.format(member), color=15548997)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            embed = discord.Embed(title='Unbanned!', description='{}'.format(user.mention), color=5814783)
            await ctx.send(embed=embed)
            return

@client.command(description='Mutes the specified user.')
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name='Muted')

    if not mutedRole:
        mutedRole = await guild.create_role(name='Muted')

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title='Muted', description=f'{member.mention} Has Been Muted! ', color=5814783)
    embed.add_field(name='reason:', value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send('You Have Been Muted from: {} reason: {}'.format(guild.name,reason))
    
@client.command(description='Unmutes a specified user.')
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   mutedRole = discord.utils.get(ctx.guild.roles, name='Muted')

   await member.remove_roles(mutedRole)
   await member.send('You Have Been Unmuted from: {}'.format(ctx.guild.name))
   embed = discord.Embed(title='Unmuted!', description=f'now you can talk! {member.mention}',color=5814783)
   await ctx.send(embed=embed)

@client.command()
async def randomhentai(ctx):
    pics = discord.Embed(color=5814783)
    randomhen = random.choice(hentai)
    pics.set_image(url=randomhen)
    await ctx.send(embed=pics)

@client.command()
async def anime(ctx):
    try:
        r = requests.get('https://myanimelist.net/search/all?q={}'.format(ctx.message.content).replace('?anime ', ''))
        soup = BeautifulSoup(r.text, 'html.parser')
        hrefs = soup.find('a', 'hoverinfo_trigger fw-b fl-l')
        animename = hrefs['href']
        await ctx.send(animename)
    except:
        await ctx.send('`Anime Not Found!`')

@client.command()
async def chara(ctx):
    try:
        r = requests.get('https://myanimelist.net/character.php?q={}&cat=character'.format(ctx.message.content).replace('?chara ', ''))
        soup = BeautifulSoup(r.text, 'html.parser')
        tablechar = soup.find('td', 'borderClass bgColor1')
        linkchara = tablechar.find('a')
        hrefs = linkchara['href']
        r2 = requests.get(hrefs)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        info = soup2.find('h1').text
        kanji = soup2.find('h2', 'normal_header').text
        await ctx.send('`{}`\n`{}`\n{}'.format(kanji, info, r2.url))
    except:
        await ctx.send('`Character Not Found!`')

@client.command()
async def wiki(ctx):
    await ctx.send('https://en.wikipedia.org/wiki/{}'.format(ctx.message.content).replace('?wiki ', ''))

@client.command()
async def randommeme(ctx):
    embed = discord.Embed(color=5814783)
    meme = random.choice(memes)
    embed.set_image(url=meme)
    await ctx.send(embed=embed)

@client.command()
async def katagaul(ctx):
    r = requests.get('https://bahasadaring.com/arti-kata?kata={}'.format(ctx.message.content).replace('?katagaul ',''))
    soup = BeautifulSoup(r.text, 'html.parser')
    if 'Waduh! Kata' in r.text:
        await ctx.send('`Maaf Kata Yang Anda Cari Tidak Ada`')
    else:
        arti = soup.find('p', 'card-text').text
        embed = discord.Embed(color=5814783)
        embed.add_field(name=ctx.message.content.replace('?katagaul', ''), value=arti)
        await ctx.send(embed=embed)

@client.command()
async def revip(ctx):
    r = requests.get('https://sonar.omnisint.io/reverse/{}'.format(ctx.message.content).replace('?revip ', ''))
    if "error:Invalid IPv4 address" in r.text:
        pass
    else:
        links = r.text
        reverse = links.replace("www.", "").replace('error:Invalid IPv4 address','').replace('api.', '').replace('cpanel.', '').replace('webmail.', '').replace('webdisk.', '').replace('ftp.', '').replace('[', '').replace('"', '').replace(',', '\n').replace('cpcalendars.', '').replace('cpcontacts.', '').replace('mail.', '').replace('ns1.', '').replace('ns2.', '').replace('ns3.','').replace('ns4.','').replace('autodiscover.', '').replace('.cdn.cloudflare.net', '').replace(']', '')
        embed = discord.Embed(title=ctx.message.content.replace('?revip', ''), description=reverse, color=5814783)
        await ctx.send(embed=embed)

client.run(TOKEN)
