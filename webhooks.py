import discord
from discord.ext import commands
import os
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

trigger_webhooks = {}

AVATARS = {
    "toji": "https://i.pinimg.com/736x/90/63/f1/9063f1b824420dcafb1a25f29e3b6330.jpg",
}

@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')
    print(f'Active triggers: {list(trigger_webhooks.keys())}')

@bot.command()
async def createtrigger(ctx, trigger_word: str):
    trigger = trigger_word.lower().strip()

    if trigger in trigger_webhooks:
        await ctx.send(f"⚠️ Trigger `{trigger}` already exists!")
        return

    avatar_url = AVATARS.get(trigger, AVATARS.get("toji"))

    try:
        webhook = await ctx.channel.create_webhook(
            name=trigger.capitalize(),
            avatar=await bot.http.get_from_cdn(avatar_url) if avatar_url else None,
            reason=f"Trigger webhook for {trigger}"
        )

        trigger_webhooks[trigger] = webhook
        await ctx.send(f"✅ Trigger `{trigger}` created!\n"
                       f"Webhook made with name **{trigger.capitalize()}** and character avatar.\n"
                       f"Usage: `{trigger} your message here` → I'll delete and repost via webhook.")

    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to create webhooks in this channel.")
    except Exception as e:
        await ctx.send(f"❌ Failed to create webhook: {str(e)}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    await bot.process_commands(message)

    content = message.content.strip()
    if not content:
        return

    words = content.split()
    if not words:
        return

    first_word = words[0].lower()

    if first_word in trigger_webhooks:
        webhook = trigger_webhooks[first_word]

        if len(words) > 1:
            response = " ".join(words[1:])
        else:
            response = "..."

        try:
            await message.delete()
        except:
            pass

        try:
            await webhook.send(
                content=response,
                username=webhook.name,
                avatar_url=webhook.avatar
            )
        except:
            await message.channel.send(response)

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        print("❌ DISCORD_TOKEN environment variable not found!")
        print("Set it in Render Dashboard → Environment Variables")
    else:
        bot.run(token)
