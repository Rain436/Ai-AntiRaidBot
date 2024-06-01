import discord
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

spam_tracker = {}

@bot.event
async def on_ready():
    print(f'{bot.user.name}')


@bot.event
async def on_message(message):

    if any(role.permissions.administrator for role in message.author.roles):
        return
    

    if message.author == bot.user:
        return
    

    if message.author.id in spam_tracker:
        spam_tracker[message.author.id] += 1
        if spam_tracker[message.author.id] > 5:  
            await message.delete()
            await message.channel.send(f"{message.author.mention} Blocked Message")
            return
    else:
        spam_tracker[message.author.id] = 1

    await bot.process_commands(message)

@bot.event
async def on_member_update(before, after):
    dangerous_roles = ["admin role", "admin role"] 
    for role in after.roles:
        if role.name in dangerous_roles:
            await after.remove_roles(role)
            await after.send("Blocked Roles.")

bot.run("YOUR_BOT_TOKEN")
