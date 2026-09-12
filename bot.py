```python
import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID', 0))

@bot.event
async def on_ready():
    print('============================')
    print(f'Logged in as {bot.user}')
    print(f'Bot ID: {bot.user.id}')
    print(f'Number of servers: {len(bot.guilds)}')
    print('Server list:')

    for guild in bot.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

    print('============================')

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        print(f'Log channel found: {log_channel.name}')

        try:
            await log_channel.send('Bot started successfully!')
        except discord.errors.Forbidden:
            print('Cannot write to the log channel')
    else:
        print('Log channel not found')

    try:
        synced = await bot.tree.sync()
        print(f'{len(synced)} commands registered')
    except Exception as e:
        print(f'Error registering commands: {e}')


@bot.tree.command(
    name="channel-info",
    description="Display information about the current channel"
)
async def channel_info(interaction: discord.Interaction):
    channel = interaction.channel

    embed = discord.Embed(
        title=f"Channel Information: {channel.name}",
        color=discord.Color.blue(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="ID",
        value=channel.id,
        inline=True
    )

    embed.add_field(
        name="Type",
        value=str(channel.type),
        inline=True
    )

    embed.add_field(
        name="Created At",
        value=channel.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        inline=True
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="server-stats",
    description="Display server statistics"
)
async def server_stats(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title=f"Server Statistics: {guild.name}",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    embed.add_field(
        name="Members",
        value=guild.member_count,
        inline=True
    )

    embed.add_field(
        name="Created At",
        value=guild.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        inline=True
    )

    embed.add_field(
        name="Channels",
        value=len(guild.channels),
        inline=True
    )

    embed.set_thumbnail(
        url=guild.icon.url if guild.icon else None
    )

    await interaction.response.send_message(embed=embed)


@bot.tree.command(
    name="set-log-channel",
    description="Set the log channel"
)
@app_commands.checks.has_permissions(administrator=True)
async def set_log_channel(
    interaction: discord.Interaction,
    channel: discord.TextChannel
):
    global LOG_CHANNEL_ID

    LOG_CHANNEL_ID = channel.id

    embed = discord.Embed(
        title="Log Channel Set",
        description=f"{channel.mention} has been set as the log channel",
        color=discord.Color.green(),
        timestamp=datetime.utcnow()
    )

    await interaction.response.send_message(embed=embed)


@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="Message Deleted",
            description=f"A message from {message.author.mention} was deleted in {message.channel.mention}",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Message Content",
            value=message.content or "No content",
            inline=False
        )

        await log_channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return

    if before.content == after.content:
        return

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="Message Edited",
            description=f"A message from {before.author.mention} was edited in {before.channel.mention}",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )

        embed.add_field(
            name="Before",
            value=before.content,
            inline=False
        )

        embed.add_field(
            name="After",
            value=after.content,
            inline=False
        )

        await log_channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="New Member",
            description=f"{member.mention} joined the server",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        embed.add_field(
            name="Account Created",
            value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            inline=False
        )

        await log_channel.send(embed=embed)


@bot.event
async def on_member_remove(member):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        embed = discord.Embed(
            title="Member Left",
            description=f"{member.mention} left the server",
            color=discord.Color.red(),
            timestamp=datetime.utcnow()
        )

        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )

        await log_channel.send(embed=embed)


@bot.event
async def on_voice_state_update(member, before, after):
    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    if log_channel:
        if before.channel != after.channel:

            if after.channel:
                embed = discord.Embed(
                    title="Voice Channel Joined",
                    description=f"{member.mention} joined {after.channel.name}",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
            else:
                embed = discord.Embed(
                    title="Voice Channel Left",
                    description=f"{member.mention} left {before.channel.name}",
                    color=discord.Color.red(),
                    timestamp=datetime.utcnow()
                )

            await log_channel.send(embed=embed)


try:
    token = os.getenv('TOKEN')

    if not token:
        raise ValueError(
            "Bot token not found. Make sure the .env file exists and is configured correctly"
        )

    channel_id = os.getenv('LOG_CHANNEL_ID')

    if not channel_id:
        raise ValueError(
            "Log channel ID not found. Make sure LOG_CHANNEL_ID exists in the .env file"
        )

    try:
        LOG_CHANNEL_ID = int(channel_id)
    except ValueError:
        raise ValueError(
            f"Invalid channel ID: {channel_id}. It must be a number"
        )

    print("Starting bot...")
    bot.run(token)

except Exception as e:
    print(f"Error: {str(e)}")
```

