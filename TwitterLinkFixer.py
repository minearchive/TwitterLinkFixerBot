import discord, argparse, re

parser = argparse.ArgumentParser(description='set token')
parser.add_argument('-token', type=str, help='set your token', default=None)

args = parser.parse_args()

token = args.token
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print("Ready to replace URL!")


@client.event
async def on_message(message):
    channel = message.channel
    if type(message.content) == str:
        if matchTwitter(message.content):
            await message.delete()
            fixed = message.content.replace("twitter.com", "fxtwitter.com")
            msg = await channel.send(f"Sent by {get_username(message.author)}.\n{fixed}")
            await msg.add_reaction('❌')
        elif matchX(message.content):
            await message.delete()
            fixed = message.content.replace("x.com", "fxtwitter.com")
            msg = await channel.send(f"Sent by {get_username(message.author)}.\n{fixed}")
            await msg.add_reaction('❌')


@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author != client.user:
        return
    if str(reaction.emoji) != '❌':
        return
    users = []
    async for userr in reaction.users():
        users.append(userr)
    if (reaction.count > 1 and client.user in users) and (user in users):
        await reaction.message.delete()
        channel = reaction.message.channel
        await channel.send(f"Link deleted by {user.name}")

def get_username(author:discord.User|discord.Member):
    if author.discriminator == "0":
        return f"@{author.name}"
    else:
        return f"{author.name}#{author.discriminator}"

def matchTwitter(search:str):
    return re.search(r'https://twitter\.com/\w+/status/\d+', search) != None

def matchX(search:str):
    return re.search(r'https://x\.com/\w+/status/\d+', search) != None

if args.token is None:
    print("Token is empty.")
else:
    client.run(token)
