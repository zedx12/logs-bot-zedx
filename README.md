## Discord Logging Bot

A Discord bot for logging and monitoring server activity.

## Features

* Log deleted and edited messages
* Log member joins and leaves
* Log voice channel activity
* Commands for viewing channel and server information
* Ability to change the log channel

## Requirements

* Python 3.8 or newer
* Discord Developer account
* Discord bot token
* Log channel ID

## Installation

### 1. Install the dependencies

```bash
pip install -r requirements.txt
```

### 2. Create a `.env` file

Add the following environment variables:

```env
TOKEN=your_bot_token_here
LOG_CHANNEL_ID=your_log_channel_id
```

### 3. Start the bot

```bash
python bot.py
```

## Deploying to Railway

1. Connect your GitHub account to Railway.
2. Create a new project and select your repository.
3. Add the environment variables `TOKEN` and `LOG_CHANNEL_ID` in the project settings.
4. Railway will automatically deploy the bot.

## Available Commands

* `/channel-info` - Display information about the current channel
* `/server-stats` - Display server statistics
* `/set-log-channel` - Set the log channel (Administrator only)

## License

This project is licensed under the MIT License.
