import discord
import argparse

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
    if ("twitter.com" in message.content) and not (
            ("fxtwitter.com" in message.content) or ("twitter.com/home" in message.content)):
        await message.delete()
        fixed = message.content.replace("twitter.com", "fxtwitter.com")
        msg = await channel.send(f"{message.author}さんが送信したリンクです。\n{fixed}")
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
    if (reaction.count >= 3 and client.user in users) and (user in users):
        await reaction.message.delete()
        channel = reaction.message.channel
        await channel.send(f"{user.name}さんが削除しました。")

if args.token is None:
    print("Token is empty.")
else:
    client.run(token)
