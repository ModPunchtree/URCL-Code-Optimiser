# main file for repl.it 

import discord
import os
from random import randint
from keep_alive import keep_alive
import asyncio
from URCLOptimiser.URCLOptimiser import URCLOptimiser
from URCLTokeniser.URCLTokeniser import URCLTokeniser

client = discord.Client()


@client.event
async def on_ready():
    print("Username: " + str(client.user))


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    elif message.content.startswith("$lol"):
        if str(message.author) == "Mod Punchtree#5817":
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")
        elif randint(1, 20) == 1:
            await message.channel.send("```\nFatal - Token too big:\nyoMamma\n      ^\n```")
        else:
            await message.channel.send(":regional_indicator_l::regional_indicator_o::regional_indicator_l:")

    elif message.content.startswith("$help") and str(message.channel) != "urcl-bot":
        await message.channel.send(":woman_shrugging:")
        return

    elif str(message.channel) != "urcl-bot":
        return

    elif message.content.startswith("$help"):
        await message.channel.send("""```c\nTo emulate URCL code do:\n$URCL\n// URCL code goes here\n\nTo compile B code to optimised URCL do:\n$B [wordLength = 8], [numberOfRegisters = 2]\n// B code goes here\n\nTo compile B code to unoptimised URCL do:\n$BAD [wordLength = 8], [numberOfRegisters = 2]\n// B code goes here\n\nTo optimise URCL code do:\n$optimise\n// URCL code goes here\n\nTo "LOL" do:\n$lol\n```""")
        return

    elif message.content.startswith("$optimise"):
        await message.channel.send("Compiling...")
        try:
            tokens, rawHeaders = URCLTokeniser(message.content[10: ])
            tokens, headers = URCLOptimiser(tokens, rawHeaders)
            text = ""
            for line in tokens:
                text += " ".join(line) + "\n"
            text = text[: -1]
        except Exception as x:
            await message.channel.send("ERROR: \n" + str(x))
            return
        f = open("output.txt", "w")
        f.write(text)
        f.close()
        await message.channel.send(file=discord.File("output.txt"))
        return

    else:
        return

keep_alive()
client.run(os.getenv("TOKEN"))
