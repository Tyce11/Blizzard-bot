from ast import alias
import discord
import asyncio
from discord.ext import commands
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch


from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Gets YT api key from .env file
load_dotenv()
yt_key = os.getenv('YT_KEY')

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.is_looping = False


        self.vc = None
    

    def query_yt(self, query):
        
        videos_search = VideosSearch(query, limit = 1)
        results = videos_search.result()

        if results['result']:
            first_video = results['result'][0]
            video_url = first_video['link']
            return video_url
        

    def search_yt(self, item):

        if not item.startswith("https://"):
            item = self.query_yt(item)
        
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                song_info = ydl.extract_info(item, download=False)
            except Exception:
                return False
        return {'source': song_info['url'], 'title':song_info['title'], 'duration': song_info['duration']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            # If loop is not active, remove the current song from the queue
            if not self.is_looping:
                self.music_queue.pop(0)

            # If there are still songs left in the queue, play the next one
            if len(self.music_queue) > 0:
                self.is_playing = True

                m_url = self.music_queue[0][0]['source']

                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            # Connect to vc if not already in one
            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    await ctx.send("Could not connect to voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])

            while True:
                self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
                await asyncio.sleep(self.music_queue[0][0]['duration'])

                # Break the loop if not in loop mode
                if not self.is_looping:
                    break
        else:
            self.is_playing = False

    @commands.command(name="play",aliases=["p","playing"], help="Play the selected song from Youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voice_channel = ctx.author.voice.channel
        if voice_channel is None: # If user is not in a vc
            await ctx.send("Connect to a voice channel")
        elif self.is_paused:
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.send("Couldn't get song!")
            else:
                await ctx.send("Song added to queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the current song")
    async def pause(self, ctx, *args):   
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()

        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
    
    @commands.command(name="resume", aliases = ["r"],help="Resumes the current song")
    async def resume(self, ctx, *args):  
        if self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
    
    @commands.command(name="skip",aliases=["s"], help="Skips the current song")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
        if len(self.music_queue) > 0:
            self.music_queue.pop(0)
        await self.play_music(ctx)

    @commands.command(name="queue",aliases=["q"], help="Displays all songs in queue")
    async def queue(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            if i > 4: break
            retval += self.music_queue[i][0]['title'] + '\n'

        if retval != "":
            await ctx.send(retval)
        else:
            await ctx.send("No music in queue")

    @commands.command(name="clear",aliases=["c"], help="Stops song and clears queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")
    
    @commands.command(name="leave",aliases=["l","disconnect","dc"], help="Kicks bot from VC")
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()
    
    @commands.command(name="loop", help="Toggle loop mode (usage: *loop or *loop off)")
    async def loop(self, ctx, *args):
        if len(args) > 0 and args[0] == "off":
            self.is_looping = False
            await ctx.send("Looping turned off")
        elif self.is_looping:
            await ctx.send("Looping already turned on")
        else:
            self.is_looping = True
            await ctx.send("Looping turned on")