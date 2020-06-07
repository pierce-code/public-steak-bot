import discord
from discord import member
from discord import emoji
from discord.utils import get
from discord.ext import commands
import random as rand
import sys, traceback
from secret import getSecret
import time

def get_prefix(client, message):
    prefixes = ['$steak ', '$s ']
    return commands.when_mentioned_or(*prefixes)(client, message)

bot = commands.Bot(
    command_prefix=get_prefix,
    description='A bot for managing TheMisteakHouse discord server',
    owner_id=174283676043968512,
    case_insensitive=True
)
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} - {bot.user.id}')

@bot.listen()
async def permError(ctx):
    await ctx.message.channel.send("**__Error: You do not have the required permissions. Please contact the admins if you believe this is a mistake.__**")

@bot.listen()
async def checkPerm(ctx):
    f = open("admins.txt","r")
    adminList = f.read().split(",")
    f.close
    if(str(ctx.message.author.id) in adminList):
        return True
    else: 
        await permError(ctx)
        return False

@bot.event
async def on_message(message):

# This is my giant on_message event. Every time a message is sent, it goes through this thing. 
# 

    #I have no idea what this first thing is for.
    if(message.channel.id == 702218772437663744):
        ctx = await bot.get_context(message)
        rolelist = message.author.roles

    #This is for new members of the clan to join with in #start-here.
    if(message.channel.id == 681619545156354082):
        ctx = await bot.get_context(message)
        if(message.content == 'join'):
            newMember = ctx.message.author
            await newMember.add_roles(ctx.message.guild.get_role(592909672504229888))
            await newMember.remove_roles(ctx.message.guild.get_role(681924535439589388))
            await ctx.guild.get_channel(592844651577212942).send(f"Welcome {newMember.display_name} to the clan!")
            await ctx.message.delete()
    
    #This is for botSpeak.
    if (storeVars.state == 1):
        if((message.channel.id == 677272430330249429) & (message.author != bot.user)):
            ctx = await bot.get_context(message)
            if (ctx.message.content == "$s stop"):
                storeVars.state = 0
                await ctx.message.channel.send("*[BotSpeak Disabled]*")
            else:
                await ctx.guild.get_channel(storeVars.channel).send(ctx.message.content)
                await ctx.message.channel.send("*[sent]*")

    #Without this line, commands dont work. At all.
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    #This tracks reactions, currently only used for setting up events.
    #I had alot of trouble with this, as you can see by the debug prints

    #print("reaction detected")
    #print(f"reaction message id: {reaction.message.id}")
    #print(f"stored message id: {newEvent.currentEvent}")
    #print(f"reaction id: {reaction.emoji.id}")
    #print("truth emoji id: 667559795011878929")
    if ((reaction.message.id == newEvent.currentEvent) and (reaction.emoji.id == 667559795011878929)):
        newEvent.players.append(user.display_name)
        if (len(newEvent.players) == int(newEvent.numPlayers)):
            await reaction.message.channel.send("Sign up completed. Fireteam: {}".format(newEvent.players))

# Standard ping pong.
@bot.command()
async def ping(ctx):
    await ctx.channel.send("Pong!")

#requests a role from the admins.
@bot.command()
async def getRole(ctx, role):
    await ctx.message.delete()
    await ctx.channel.send(f'Thank you {ctx.message.author.name}, your request will be processed.')
    await bot.get_channel(592907620143333376).send(f'@here {ctx.message.author.display_name} has requested the role {role} in #{ctx.channel.name}')


#==============================================================================================================================
#                                  above functions are for users, below are for admins.
#==============================================================================================================================
# All admin functions must have the 'if await checkPerm(ctx):'
# before them, or all users will have access.
#==============================================================================================================================

        
#send a single message to a channel.
@bot.command()
async def msgChannel(ctx, channelId, msg):
    if await checkPerm(ctx):
        targetChannel = bot.get_channel(int(channelId))
        await targetChannel.send(msg)

#sets up a new event
@bot.command()
async def newEvent(ctx, numPlayers, msg):
    if await checkPerm(ctx):
        form = await ctx.guild.get_channel(670382340513464353).send("{} React with the :truth: emoji to sign up! Limit is {} players.".format(msg, numPlayers))
        # I would use the storeVars class for this but somehow storing variables
        # in this method works, but storing variables in other methods doesnt.
        # very weird, should move to storeVars at somne point
        newEvent.currentEvent = form.id
        newEvent.players = []
        newEvent.numPlayers = numPlayers
        print(form.id)
        
#tests permissions.
@bot.command()
async def test(ctx):
    if await checkPerm(ctx):
        await ctx.message.channel.send("You have the permissions for this.")

#turns on botSpeak (see on_message event)
@bot.command()
async def botSpeak(ctx, channel):
    if await checkPerm:
        storeVars.state = 1
        storeVars.channel = int(channel)
        await ctx.message.channel.send("*[BotSpeak enabled, to end type `$s stop`]*")

class storeVars:
    #literally used to store variables and thats it

    # state 1 is on, 0 is off
    state = 0
    channel = 0



bot.run(getSecret(), bot = True, reconnect = True)