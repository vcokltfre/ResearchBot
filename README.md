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

class command_roles:
    lvl0roles = ['Administrator', 'Moderator', 'Senior Moderator', 'Staff', 'Private Project Access',
                'Private Chat Access', 'Member']
    lvl1roles = ['Administrator', 'Moderator', 'Senior Moderator', 'Staff', 'Private Project Access',
                'Private Chat Access']
    lvl2roles = ['Administrator', 'Moderator', 'Senior Moderator', 'Staff', 'Private Project Access']
    lvl3roles = ['Administrator', 'Moderator', 'Senior Moderator', 'Staff']
    lvl4roles = ['Administrator']

nick_request_channel_id = channel_id
nick_accept_channel_id = channel_id

yourlspw="your yourls password" #You probably dont want this, so you may want to comment out the line that says "bot.cogs.utility.links" in main.py
welcome_channel = welcome_channel_id
```