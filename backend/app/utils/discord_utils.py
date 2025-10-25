import requests
import discord
from app.core.config import settings

def dc_send_webhook(message: str, webhook_url: str) -> bool:
    """Send message to Discord using webhook URL."""
    try:
        payload = {"content": message}
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Message sent successfully via webhook")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message via webhook: {e}")
        return False

def dc_send(message: str, token: str, guild_id: int, channel_id: int):
    """Send a message to a Discord channel using bot."""
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        guild = discord.utils.get(client.guilds, id=guild_id)
        if guild is None:
            print(f'Guild with ID {guild_id} not found')
            await client.close()
            return

        channel = discord.utils.get(guild.channels, id=channel_id)
        if channel is None:
            print(f'Channel with ID {channel_id} not found in guild {guild_id}')
            await client.close()
            return

        await channel.send(message)
        await client.close()

    client.run(token)

def send_discord_message(message: str):
    """Send message to Discord using webhook if available, otherwise use bot."""
    if settings.DISCORD_WEBHOOK_URL:
        success = dc_send_webhook(message, settings.DISCORD_WEBHOOK_URL)
        if success:
            return
    
    if settings.DISCORD_TOKEN and settings.DISCORD_GUILD_ID and settings.DISCORD_CHANNEL_ID:
        dc_send(message, settings.DISCORD_TOKEN, settings.DISCORD_GUILD_ID, settings.DISCORD_CHANNEL_ID)
