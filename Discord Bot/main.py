import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv ("DISCORD_BOT_TOKEN") 

if token is None:
    print("❌ ERROR: DISCORD_BOT_TOKEN not found in .env")
else:
    print("✅ Token loaded successfully")
    

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default() 
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents) 

secret_role = "Member"


@bot.event
async def on_ready():
    print(f"We are Ready to go in, {bot.user.name}")
    
@bot.event   
async def on_member_join(member):
    await member.send(f"Welcome to the server, {member.name}!") 
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if "fuck" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention}, Chup thako beyadop!")
    await bot.process_commands(message)
    
    
@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello, {ctx.author.mention}!")  
    
@bot.command()
async def assign(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.add_roles(role)
        await ctx.send(f"{ctx.author.mention}, you have been given the {secret_role} role!")
    else:
        await ctx.send(f"Role {secret_role} doesn't exist.")
        
        
@bot.command()
async def remove(ctx):
    role = discord.utils.get(ctx.guild.roles, name=secret_role)
    if role: 
        await ctx.author.remove_roles(role)
        await ctx.send(f"{ctx.author.mention}, has had the {secret_role} removed!")
    else:
        await ctx.send(f"Role {secret_role} doesn't exist.")
        
        
@bot.command()
async def dm(ctx , * , msg):
    await ctx.author.send(f"You said {msg}")
    

@bot.command()
async def reply(ctx):
    await ctx.reply("This is a reply to your command!")
    
    
@bot.command()
async def poll(ctx, * , question):
    embed = discord.Embed(title="New Poll", description=question, color=0x00ff00)
    poll_number = await ctx.send(embed=embed)
    await poll_number.add_reaction("🎀")
    await poll_number.add_reaction("🙏")
    
    
    
    
        
@bot.command()
@commands.has_role(secret_role)
async def secret(ctx):
    await ctx.send("Welcome to the secret club!")
@secret.error
async def secret_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("You do not have the required role to access this command.")
    
    

bot.run(token, log_handler=handler, log_level=logging.DEBUG)  



 

