# Blizzard-bot

Welcome to Blizzard bot! A Discord bot that is easy to use and also easy to customize! Currently, the bot delivers exceptional music playback features, allowing you to use YouTube links to play music in your Discord voice chat.

## Prerequisites

+ Python3 and Pip
+ [Discord bot token](https://discordgsm.com/guide/how-to-get-a-discord-bot-token)
+ [YouTube API Key](https://developers.google.com/youtube/registering_an_application)
+ [FFMPEG (Windows)](https://phoenixnap.com/kb/ffmpeg-windows)
+ [FFMPEG (Ubuntu)](https://phoenixnap.com/kb/install-ffmpeg-ubuntu)

## Installation

Make the directory you want your bot to be in <br>
`mkdir my-bot`

Move into your directory <br>
`cd my-bot`

Clone the repository <br>
`git clone https://github.com/Tyce11/Blizzard-bot.git`

Install the required dependencies <br>
`pip install -r requirements.txt`

Create your .env file <br>
Linux: `touch .env`
Windows: `echo > .env`

Open your .env file <br>
Linux: `nano .env` 
Windows: `notepad .env`

Add your two keys <br>
`TOKEN='Your-Discord-Token'` <br>
`YT_Key='Your-YouTube-Token'`

Run main.py <br>
`python3 /path/to/main.py`

## Contributing 

Contributions are welcomed! If you have a cool feature in mind or found a bug, please create a pull request or raise an issue on this GitHub repository. 

## Known Issues/limitations 

+ Bot has difficulty playing songs that are part of a playlist
+ If bot sits AFK in a VC it will no longer play newly requested songs
  
## Note

Blizzard Bot is currently in active development. Stay tuned for updates and new features! 
