import os
import asyncio
import datetime
import requests
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands



load_dotenv()
DEV = 954419840251199579
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", description="big orbusz", intents=intents)


async def devcheck(interaction: discord.Interaction):
    if interaction.user.id == DEV:
        return True
    else:
        await errorrespond(interaction, f"Only <@{DEV}> is allowed to use this command")
        return False
    

def errorembed(error: str):
    embed = discord.Embed(color=0xFF6700)
    embed.add_field(name="Error", value=error, inline=False)
    return embed


async def errorrespond(interaction: discord.Interaction, error: str):
    await interaction.response.send_message(embed=errorembed(error), ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")    


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="sync", description="sync the command tree")
async def sync_cmd(interaction: discord.Interaction):
    if not await devcheck(interaction):
        return
    await interaction.response.defer(ephemeral=True)
    cmds = await bot.tree.sync()
    for cmd in cmds:
        print(f"Command synced: {cmd}")
    print("Command tree synced")
    await interaction.followup.send("Command tree synced")

@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="forint", description="eur to huf")
async def forint_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    today_utc = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
    yesterday_utc = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    today_rates = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{today_utc}/v1/currencies/eur.json").json()
    yesterday_rates = requests.get(f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{yesterday_utc}/v1/currencies/eur.json").json()

    today_forint = today_rates["eur"]["huf"]
    yesterday_forint = yesterday_rates["eur"]["huf"]
    is_it_viktover = today_forint > yesterday_forint

    await interaction.followup.send(f"Euro is {round(today_forint, 4)} Forints... " + ("It's Viktóver... :pensive:" if is_it_viktover else "Glory to Hungary! :flag_hu:"))



bot.run(os.getenv("TOKEN"))
