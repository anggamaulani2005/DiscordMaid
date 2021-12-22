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

hentai = [
    'link.com'
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
