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

def OwO(content):
    sentence = ""
    for letter in content:
        if letter == "r" or letter =="l":
            letter = "w"
        sentence+=letter
    return sentence


@client.event
async def on_ready():
    print("$$$$$")
    global Start_Time
    activity = discord.Game(name="dead")
    await client.change_presence(status=discord.Status.online, activity=activity)
    Start_Time = datetime.datetime.now()

@client.command()
async def cs(ctx):
    msg = await ctx.channel.send("<@&691037783074144296>cs?")
    await msg.add_reaction('🇾')
    await msg.add_reaction('🇳')

@client.command()
async def simon(ctx):
    gameLoop = True
    past_index = 5
    level = 1
    Pattern = []
    Colors = []
    squares = ['🟩','🟥','NULL','🟨','🟦','⬜']
    DefBoard = ['🟩','🟥','\n','🟨','🟦']
    Board = ['🟩','🟥','\n','🟨','🟦']
    Cube = await ctx.channel.send("".join(DefBoard))
    msg = await ctx.channel.send("Starting in 3 seconds")
    while gameLoop:

        index = random.randint(0,4)
        while index == past_index or index == 2:
            index = random.randint(0,4)
        if index == 0:
            value = 'G'
        elif index == 1:
            value = 'R'
        elif index == 3:
            value = 'Y'
        else:
            value = 'B'
        Colors.append(value)
        Pattern.append(str(index))
        past_index = index


        await asyncio.sleep(3)
        await msg.delete()
        for i in range(level):
            Board[int(Pattern[i])] = squares[5]
            await Cube.edit(content="".join(Board))
            await asyncio.sleep(1)
            Board[int(Pattern[i])] = squares[int(Pattern[i])]
        await Cube.edit(content="".join(DefBoard))
        print("".join(Colors))

        msg = await client.wait_for('message')
        while msg.author != ctx.author:
            msg = await client.wait_for('message')
        if str(msg.content) == str("".join(Colors)):
            await msg.delete()
            msg = await ctx.channel.send("Correct. Shuffling the board in 3 seconds")
            level += 1
        else:
            Solution = " ".join(Colors)
            await ctx.channel.send(f"You lose! The pattern was {Solution}. Final score = {level - 1}")
            gameLoop = False


@client.event
async def on_voice_state_update(member,before, after):
    if after.channel.id == 695365204057391105 and before.channel.id != 695365204057391105 and member.id == 157558511692283904:
        await after.channel.edit(name='biuk is here')
    if before.channel.id == 695365204057391105 and after.channel.id != 695365204057391105 and member.id == 157558511692283904:
        await before.channel.edit(name='biuk is not here')
    if member.id == 150335981961216000 or member.id == 205453758069473280 and after.channel == None:
        channel = client.get_channel(417039633122328606)
        await channel.send(f"Bye <@{member.id}>")
    if after.channel.id == 695365204057391105 and member.nick != 'biuk':
        pastNick = member.nick
        username = member
        await member.edit(nick='biuk')
        await client.wait_for('voice_state_update')
        while True:
            if member == username and after.channel == None or after.channel.id != 695365204057391105:
                await member.edit(nick=pastNick)
                break
            else:
                await client.wait_for('voice_state_update')
@client.command()
async def hangman(ctx,*args):
    await ctx.message.delete()
    #Functions
    #Winning function
    async def win():
        await SentWord.edit(content=Failure)
        await ctx.channel.send("You win")
        return 0
    #Losing function
    async def lose():
        if used:
            await used.delete()
        await guess.delete()
        await ctx.channel.send("Incorrect guess. Game Over")
        await SentWord.edit(content=Failure)
        return 0
    #Input sorting function
    async def checkInput(Input,AllowedInput):
        Input = Input.strip()
        if Input[0] == '|' and Input[1] == '|' and Input[len(Input)-1] == '|' and Input[len(Input)-2] == '|':
            for i in range(2,len(Input)-2):
                print(Input[i])
                if Input[i].upper() not in AllowedInput and Input[i] != ' ':
                    return False
            return True
        else:
            return False
    #Hangman Pictures
    HangmanPic = [
    'https://upload.wikimedia.org/wikipedia/commons/8/8b/Hangman-0.png',
    'https://upload.wikimedia.org/wikipedia/commons/3/30/Hangman-1.png',
    'https://upload.wikimedia.org/wikipedia/commons/7/70/Hangman-2.png',
    'https://upload.wikimedia.org/wikipedia/commons/9/97/Hangman-3.png',
    'https://upload.wikimedia.org/wikipedia/commons/2/27/Hangman-4.png',
    'https://upload.wikimedia.org/wikipedia/commons/6/6b/Hangman-5.png',
    'https://upload.wikimedia.org/wikipedia/commons/d/d6/Hangman-6.png'
    ]
    #Rules
    Health = 0
    embed = discord.Embed(
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url=f"https://upload.wikimedia.org/wikipedia/commons/8/8b/Hangman-{Health}.png")


    #Block dedicated to creating needed variables and lists
    used = None
    Failure = ''
    GameLoop = True
    UsedLetters = []
    Emotes = ['🌀','➖'] #Fill in blank positions
    NewMsg = [] #Used to edit message after guesses
    UsedMsg = '**USED CHARACTERS: ** '
    AllowedInput = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','1','2','3','4','5','6','7','8','9','0']
    EmotesInput = ['🇦','🇧','🇨','🇩','🇪','🇫','🇬','🇭','🇮','🇯','🇰','🇱','🇲','🇳','🇴','🇵','🇶','🇷','🇸','🇹','🇺','🇻','🇼','🇽','🇾','🇿',"1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","0️⃣"]

    #Block dedicated to getting and sorting user input
    Input = " ".join(args)  #Get the full input
    if await checkInput(Input,AllowedInput):
        sentence = Input[2:len(Input)-2].upper() #Remove ||
        LettersLeft = len((sentence.replace(" ","")))
    else:
        await ctx.channel.send("```Incorrect input, proper input --> ||The sentence you want to send||```")
        return 0


    #Fill out the final sentence with emotes , sent after HP = 0
    for i in range(len(sentence)):
        if sentence[i] != ' ':
            Failure += EmotesInput[AllowedInput.index(sentence[i].upper())] + ' '
        else:
            Failure += Emotes[1]


    #Code the message using emojis
    HiddenMsg = ''
    for i in range(len(sentence)):
        if sentence[i] == ' ':
            HiddenMsg += Emotes[1]
        else:
            HiddenMsg += Emotes[0]
    Rules = await ctx.channel.send(embed=embed)
    SentWord = await ctx.channel.send(HiddenMsg)
    UsedL = await ctx.channel.send(UsedMsg)
    #Game Loop
    while GameLoop:
        guess = await client.wait_for('message')
        while guess.content.startswith("-") is False:
            guess = await client.wait_for('message')
        #Check if guess is in the sentence
        if guess.content.upper().startswith("-GUESS"):
            if guess.content.upper()[7:] == sentence:
                await win()
                return 0
            else:
                await lose()
                return 0


        if guess.content[1].upper() in AllowedInput and len(guess.content) == 2 :
            if guess.content[1].upper() not in UsedLetters:
                UsedLetters.append(guess.content[1].upper())
                UsedMsg += EmotesInput[AllowedInput.index(guess.content[1].upper())] + ' '
                await UsedL.edit(content=UsedMsg)
                #await SentWord.add_reaction(EmotesInput[AllowedInput.index(guess.content[1].upper())])
                if guess.content[1].upper() in sentence:
                    for i in range(len(HiddenMsg)):
                        NewMsg.append(HiddenMsg[i])
                    HiddenMsg = ''
                    for i in range(len(sentence)):
                        if guess.content[1].upper() == sentence[i]:
                            NewMsg[i] = EmotesInput[AllowedInput.index(guess.content[1].upper())] + ' '
                            HiddenMsg += NewMsg[i]
                            LettersLeft -=1
                            if LettersLeft <=0:
                                await ctx.channel.send("You win")
                                return 0
                        else:
                            HiddenMsg += NewMsg[i]

                else:
                    Health += 1
                    if Health >= 6:
                        embed.set_thumbnail(url=f"{HangmanPic[Health]}")
                        await Rules.edit(embed=embed)
                        await lose()
                        return 0
                    else:

                        embed.set_thumbnail(url=f"{HangmanPic[Health]}")
                        await Rules.edit(embed=embed)
            else:
                if used:
                    await used.delete()
                used = await ctx.channel.send(f"{guess.content[1].upper()} has been used before")

        await guess.delete()
        await SentWord.edit(content=HiddenMsg)
@client.command()
async def roll(ctx,*args):
    if len(args) == 2:
        if args[0].isnumeric() and args[1].isnumeric():
            if int(args[0]) > int(args[1]) :
                min = int(args[1])
                max = int(args[0])
            else:
                min = int(args[0])
                max = int(args[1])
            await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(min,max)}**")
        else:
            await ctx.channel.send("**Bad Input, type &roll ? for help**")
    elif len(args) == 1:
        if args[0].isnumeric():
            if int(args[0]) >= 0:
                await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(0,int(args[0]))}**")
            else:
                await ctx.channel.send("**Bad Input, type &roll ? for help**")
        elif args[0] == '?':
            embed = discord.Embed(
                title = "&roll",
                colour = discord.Colour.blue()
            )
            embed.add_field(name=f"**&roll #1 #2**", value="**Roll in range of #1 & #2**", inline= False)
            embed.add_field(name=f"**&roll #1**", value="**Roll in range of 0 & #1**", inline= False)
            embed.add_field(name=f"**&roll**", value="**Roll in range of 1 & 100**", inline= False)
            await ctx.channel.send(embed=embed)

        else:
            await ctx.channel.send("**Bad Input, type &roll ? for help**")
    elif len(args) == 0:
        await ctx.channel.send(f"**{ctx.author.nick} has rolled a {random.randint(1,101)}**")
    else:
        await ctx.channel.send("**Bad Input, type &roll ? for help**")


@client.event
async def on_message(message):
    global channel
    channel = message.channel
    if message.channel.id != 555040966525059072:
        print('{} - {}'.format(message.author,str(message.content)))
    if 'kms' in message.content:
        await channel.send("Do it pussy you won't")
    if message.content.upper() == 'MA':
        await channel.send("ma mia")
    if message.content.startswith("I'm ") or message.content.startswith("I am "):
        if message.content.startswith("I'm "):
            await channel.send(f"Hi {str(message.content)[4:]}! I'm Dad <:peepoDab:639947762120785930>")
        else:
            await channel.send(f"Hi {str(message.content)[5:]}! I'm Dad <:peepoDab:639947762120785930>")
    if 'ocelto' in message.content and ':ocelto:' not in message.content:
        await channel.send("<:ocelto:501865489442799616>")
    await client.process_commands(message)

@client.event
async def on_member_update(before,after):
    server = client.get_guild(212958936972656640)
    if before.guild == server:
        #print(after.nick)
        if after.nick != "ivan" and after.id == 1:
            await after.edit(nick="ivan")
        if before.status != after.status:
            Time = datetime.datetime.now()
            minute = Time.minute if Time.minute >= 10 else '0' + str(Time.minute)
            channel = client.get_channel(555040966525059072)
            print(f"{before.name} : {before.status} --> {after.status} ")
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
        await asyncio.sleep(60)

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
    ignored =  ["✉️","🐺"]
    if reaction.emoji not in ignored:
        await message.add_reaction(reaction.emoji)
    if reaction.emoji == "🐺":
        await reaction.message.channel.send(OwO(str(reaction.message.content)))
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
    embed.add_field(name=f"**&roll**", value=f"**&roll**", inline= False)
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
