#A discord bot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import time
import datetime
import calendar
import re
from datetime import date
from datetime import datetime as dt,timedelta


client = commands.Bot(command_prefix = "&")
client.remove_command('help')

@client.event
async def on_ready():
    print("$$$$$")
    global Start_Time
    activity = discord.Game(name="dead")
    await client.change_presence(status=discord.Status.online, activity=activity)
    Start_Time = datetime.datetime.now()

@client.event
async def on_message(message):
    global channel
    channel = message.channel
    print('{} - {}'.format(message.author,str(message.content)))
    if 'kms' in message.content:
        await channel.send("Do it pussy you won't")
    if message.content.upper() == 'MA':
        await channel.send("ma mia")
    if 'ocelto' in message.content and ':ocelto:' not in message.content:
        await channel.send("<:ocelto:501865489442799616>")
    await client.process_commands(message)

@client.event
async def on_member_update(before,after):
    server = client.get_guild(212958936972656640)
    if before.guild == server:
        Time = datetime.datetime.now()
        minute = Time.minute if Time.minute >= 10 else '0' + str(Time.minute)
        channel = client.get_channel(555040966525059072)
        await channel.send(f"```asciidoc\n= {before.name} : {before.status} --> {after.status} at {Time.hour}:{minute}```")

@client.event
async def on_reaction_add(reaction,user):
    message = reaction.message
    if reaction.emoji != "✉️":
        await message.add_reaction(reaction.emoji)

@client.command()
async def uptime(ctx):
    Current_Time = datetime.datetime.now()
    Time = dt(1,1,1) + timedelta(seconds=int((Current_Time - Start_Time).total_seconds()))
    await channel.send(f"```DAYS:HOURS:MIN:SEC\n{Time.day-1}:{Time.hour}:{Time.minute}:{Time.second}```")
@client.command()
async def help(ctx):
    RemindMeExample = "&remindme 20 write help command"
    CountdownExample = "&countdown 5"
    Quotes = "```"
    await ctx.channel.send(f"{Quotes}yaml\n&remindme 'minutes' 'text' --> example --> {RemindMeExample}\n&TTT\n&countdown 'minutes' --> example --> {CountdownExample}\n&killingfloor2\n&stopwatch\n&uptime{Quotes}")


@client.command()
async def remindme(ctx,*message):
    channel = ctx.channel
    try:
        await ctx.message.delete()
        TimeT = float(message[0])
        Content = ' '.join(message[1:])
        if float(TimeT) < 1:
            Time = float(TimeT * 60)
            Time_Value = "second(s)"
        else:
            Time = TimeT
            Time_Value = "minute(s)"
        msg = await channel.send(f"Noted, I will message you in {int(Time)} {Time_Value}")
        await asyncio.sleep(float(TimeT*60))
        await msg.delete()
        await channel.send(f"```{Content}``` \n <@{ctx.author.id}>")
    except:
        await channel.send('```Syntax = &remindme "Number of minutes" "Message you want sent to you"```\nEnter a valid number')

@client.command()
async def killingfloor2(ctx):
    await channel.send("Still in a few days")

@client.command()
async def TTT(ctx):
    channel = ctx.channel
    Tracker = 0
    Player_One = ":blue_circle:"
    Player_Two = ":x:"
    Board = [':zero:',':one:',':two:',':three:',':four:',':five:',':six:',':seven:',':eight:']
    Proper_inputs=['-0','-1','-2','-3','-4','-5','-6','-7','-8']
    Used_nums=[]
    await channel.send('Who else is playing? Type "Me" to join in')
    opponent = await client.wait_for('message')
    while opponent.content.upper() != 'ME':
        opponent= await client.wait_for('message')
    opponent = opponent.author
    async def print_cross(tic_tac_toe):
                row1=''.join(tic_tac_toe[:3])
                row2=''.join(tic_tac_toe[3:6])
                row3=''.join(tic_tac_toe[6:9])
                To_Say = f"{row1}\n{row2}\n{row3}\n"
                GameBoard = await channel.send(To_Say)
                return GameBoard
    def Assign(Board,Input,Player):
        if Player == Player_Two:
            Board[Input] = Player_Two
        else:
            Board[Input] = Player_One
    async def place_x(Board,Used_nums,Tracker):
        if Tracker % 2 == 0:
            Player = Player_Two
            Input = await client.wait_for('message')
            while Input.author != ctx.message.author:
                Input = await client.wait_for('message')
        else:
            Player = Player_One
            Input = await client.wait_for('message')
            while Input.author != opponent:
                Input = await client.wait_for('message')
        if Input.content in Used_nums:
            await channel.send("Space is occupied")
            return 0
        elif Input.content in Proper_inputs:
            Assign(Board,int(Input.content[1]),Player)
            Used_nums.append(Input.content)
            await Input.delete()
            return Player
        else:
            return 0
    GameBoard = await print_cross(Board)

    async def Win(Board):
        win_conditions = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        for i in range(0,8):
                if (Board[win_conditions[i][0]] == Board[win_conditions[i][1]] == Board[win_conditions[i][2]]):
                    return True

    while True:
            Player = await place_x(Board,Used_nums,Tracker,)
            if Player != 0:
                await GameBoard.delete()
                GameBoard = await print_cross(Board)
                Tracker += 1

            Exit = await Win(Board)
            if Exit:
                await channel.send(f"{Player} is the winner")
                break
            elif len(Used_nums) >=9:
                await channel.send("Draw")
                break

@client.command()
async def countdown(ctx,message):
    try:
        Time = float(message)
        Msg = await ctx.channel.send(f"Countdown of {Time} minute(s) has started")
        await asyncio.sleep(float(Time)*60)
        await Msg.delete()
        await ctx.channel.send(f"<@{ctx.author.id}> - Countdown of {Time} minute(s) has ended!")
    except:
        await ctx.channel.send("Invalid input")

@client.command()
async def stopwatch(ctx):
    Msg = await ctx.channel.send("Stopwatch has begun, type End Stopwatch to end it")
    Start_Time = datetime.datetime.now()
    Stop = await client.wait_for('message')
    print("Hello {}".format(Stop.author))
    while Stop.content.upper() != 'END STOPWATCH' or Stop.author != ctx.message.author:
        Stop = await client.wait_for('message')
    Current_Time = datetime.datetime.now()
    await Msg.delete()
    await ctx.channel.send(f"Stopwatch has ended, {int((Current_Time-Start_Time).total_seconds())} seconds have passed")

client.run(os.getenv('TOKEN'))
