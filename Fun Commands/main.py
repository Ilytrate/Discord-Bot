import discord
from discord import app_commands
import random
import os
import asyncio
from aiohttp import web

# --------------------- BOT SETUP ---------------------
intents = discord.Intents.default()
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# --------------------- GAY METER COMMAND ---------------------
@tree.command(name="gay", description="Check how gay someone is 🏳️‍🌈")
@app_commands.describe(member="The person to check (leave blank for yourself)")
async def gay_meter(interaction: discord.Interaction, member: discord.Member = None):
    if member is None:
        member = interaction.user

    # Generate gay percentage (0-100)
    gay_percentage = random.randint(0, 100)

    # Funny comments based on percentage
    if gay_percentage == 0:
        comment = "Straight as an arrow ⚡ No homo detected!"
    elif gay_percentage <= 20:
        comment = "Barely gay... practically straight 😌"
    elif gay_percentage <= 40:
        comment = "A little sus... but still safe 😏"
    elif gay_percentage <= 60:
        comment = "Mid-tier gay. Acceptable levels 🔥"
    elif gay_percentage <= 80:
        comment = "Certified homosexual 🏳️‍🌈 Getting dangerous!"
    elif gay_percentage <= 99:
        comment = "Extremely gay. Professional level 🌈"
    else:
        comment = "MAXIMUM GAY!!! YOU ARE THE GAYEST OF THEM ALL 🏳️‍🌈💦"

    # Create the embed (Orange color)
    embed = discord.Embed(
        title="🏳️‍🌈 Gay Meter",
        description=f"**{member.display_name}** is **{gay_percentage}%** gay!",
        color=0xFF8000  # Orange
    )

    embed.add_field(name="Verdict", value=comment, inline=False)

    # Command runner's profile picture in the top right
    embed.set_author(
        name=f"Requested by {interaction.user.display_name}",
        icon_url=interaction.user.display_avatar.url
    )

    # Target's avatar as thumbnail
    embed.set_thumbnail(url=member.display_avatar.url)

    embed.set_footer(text="Results may vary • Not scientifically accurate 😂")

    await interaction.response.send_message(embed=embed)


# --------------------- BOT EVENTS ---------------------
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await tree.sync()
        print(f"✅ Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")


# --------------------- RENDER WEB SERVER (Required for Render) ---------------------
async def health_check(request):
    return web.Response(text="Gay Meter Bot is running! 🏳️‍🌈")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render automatically provides the PORT environment variable
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"🌐 Web server running on port {port}")


# --------------------- START BOT ---------------------
async def main():
    # Get token from Render Environment Variables
    token = os.getenv("DISCORD_TOKEN")
    
    if not token:
        print("❌ ERROR: DISCORD_TOKEN environment variable not found!")
        return

    # Start web server and bot together
    await asyncio.gather(
        run_web_server(),
        bot.start(token)
    )

if __name__ == "__main__":
    asyncio.run(main())
