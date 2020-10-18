# vcokltfre/ResearchBot

### Setup for development

- Clone the repository and change to its directory
- Create a directory called `config`
- Under `config/` create a new file called `config.py`
- In this file create the following:
```py
name = 'ResearchBot'
log_level = 'info'
log_type = 'text'
token = 'your discord bot token'
hook = 'logging webhook url'
dev_ids = [your_discord_id]
guild = your_guild_id

nick_request_channel_id = channel_id
nick_accept_channel_id = channel_id

yourlspw="your yourls password" #You probably dont want this, so you may want to comment out the line that says "bot.cogs.utility.links" in main.py
```