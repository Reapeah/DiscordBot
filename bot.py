#A discord bot

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import numpy as np
import os
import time
import datetime
import calendar
import re
from datetime import date
from datetime import datetime as dt,timedelta


client = commands.Bot(command_prefix = "&")
client.remove_command('help')

def createEmbed(CustomTitle,Footer,User,Thumbnail,NumOfFields,Author,Field,Inline):
    print("made it")
    embed = discord.Embed(
        title = CustomTitle,
        colour = discord.Colour.blue()
    )
    embed.set_footer(text= Footer)
    embed.set_author(name= Author)
    embed.set_thumbnail(url= Thumbnail)

    for i in range(0,NumOfFields):
        embed.add_field(name=f"**{Field[i][0]}**", value=f"**{Field[i][1]}**", inline= Inline)
    return embed

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
        if before.status != after.status:
            Time = datetime.datetime.now()
            minute = Time.minute if Time.minute >= 10 else '0' + str(Time.minute)
            channel = client.get_channel(555040966525059072)

            def CheckStatus(Status):
                if Status == 'idle':
                    newStatus = ":orange_circle:"
                elif Status == 'online':
                    newStatus = ":green_circle:"
                elif Status == 'offline':
                    newStatus = ':black_circle:'
                elif Status == 'dnd':
                    newStatus = ':red_circle:'
                return newStatus
            BStatus = CheckStatus(str(before.status))
            AStatus = CheckStatus(str(after.status))

            User = f"{before.name}"
            Inline = True
            Footer = f"@{Time.hour}:{minute}"
            Thumbnail = f"https://cdn.discordapp.com/avatars/{before.id}/{before.avatar}.png?size=1024"
            FirstField = ["Before",f"{BStatus} "]
            SecondField = ["After",f"{AStatus} "]
            Field = []
            Field.append(FirstField)
            Field.append(SecondField)
            embed = createEmbed(User,Footer,'',Thumbnail,2,'',Field,Inline)
            await channel.send(embed=embed)
@client.command()
async def poll(ctx):
    try:
        numbers = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟","0️⃣"]
        counter = 0
        votes = []
        winners = []

        #User input goes here
        botmsg = await ctx.channel.send("Enter poll title")
        title = await client.wait_for('message')
        while title.author != ctx.message.author:
            title = await client.wait_for('message')
        await title.delete()
        await botmsg.delete()
        botmsg = await ctx.channel.send("Enter poll options seperated by |")
        msg = await client.wait_for('message')
        while msg.author != ctx.message.author:
            msg = await client.wait_for('message')
        await msg.delete()
        await botmsg.delete()

        #Creating poll options
        options = msg.content.split("|")
        if len(options) > 9:
            await ctx.channel.send("Limited to 9 inputs")
            return 0;
        Footer = "Powered by Monster Energy ☠"
        Author = f"Poll made by {ctx.author.display_name}"
        Field = []
        Inline = True
        for i in range(0,len(options)):
            temp = options[i].lstrip(' ')
            AppendThis = [f"Option #{i+1}",f"{temp}"]
            Field.append(AppendThis)
            votes.append(0)
        embed = createEmbed(title.content,Footer,'','',len(options),Author,Field,Inline)
        poll = await ctx.channel.send(embed=embed)

        #Adding reactions
        for temp in options:
            await poll.add_reaction(numbers[counter])
            counter+=1
        await asyncio.sleep(5)

        #Getting reactions
        message = await channel.fetch_message(poll.id)
        for reaction in message.reactions:
            async for user in reaction.users():
                if user != poll.author:
                    for i in range(0,len(numbers)):
                        if reaction.emoji == numbers[i]:
                            votes[i]+=1

        maxVal = max(votes)

        def combine(input,numbers):
            combiner = " "
            emote_list = []
            for i in range(0,len(input)):
                index = int(input[i])-1
                emote_list.append(numbers[index])
            return(combiner.join(emote_list))

        for i in range(0,len(votes)):
            if votes[i] == maxVal:
                winners.append(str(i+1))


        winner = combine(winners,numbers)
        if(len(winners)) > 1:
            Title = f"Tie between options {winner} with {maxVal} vote(s)"
            embeded = createEmbed(Title,'','','',0,'','',True)
            await ctx.channel.send(embed=embeded)
        else:
            Title = f"The winner is option {winner} with {maxVal} vote(s)"
            embeded = createEmbed(Title,'','','',0,'','',True)
            await ctx.channel.send(embed=embeded)
    except:
        await ctx.channel.send("Something went wrong")

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
    embed = discord.Embed(
        title = "Available commands",
        colour = discord.Colour.blue()
    )
    embed.set_footer(text="Powered by a very fast hamster")
    embed.set_thumbnail(url=f"https://cdn.discordapp.com/avatars/{ctx.author.id}/{ctx.author.avatar}.png?size=1024")
    embed.set_author(name= f"Called by {ctx.author.display_name}")
    embed.add_field(name=f"**&TTT**", value=f"**&TTT**", inline= False)
    embed.add_field(name=f"**&uptime**", value=f"**&uptime**", inline= False)
    embed.add_field(name=f"**&stopwatch**", value=f"**&stopwatch**", inline= False)
    embed.add_field(name=f"**&countdown**", value=f"**{CountdownExample}**", inline= False)
    embed.add_field(name=f"**&killingfloor2**", value=f"**&killingfloor2**", inline= False)
    embed.add_field(name="**&remindme**", value=f"**{RemindMeExample}**", inline= False)
    embed.add_field(name=f"**&poll**", value=f"**&poll --> Name of poll --> Option 1 | Option 2 | Option 3**", inline= False)

    await ctx.channel.send(embed=embed)

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
