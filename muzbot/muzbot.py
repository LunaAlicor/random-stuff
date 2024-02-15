import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import disnake
import requests
from bs4 import BeautifulSoup
import os
import asyncio
import youtube_dl
from moviepy.editor import *
import aiofiles


token = 'ой'

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='#', intents=intents)
music_folder = os.path.abspath(os.path.join("music"))


def download_audio_from_youtube(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info_dict = ydl.extract_info(url, download=False)
        video_title = info_dict.get('title', None).lower() + ".mp3"
        video_title = video_title.replace("/", "_")
        with open("ta_daun.txt", "w") as file:
            file.write(video_title)
        video_path = os.path.join(output_path, video_title)
        for filename in os.listdir("."):
            if filename.endswith(".mp3"):
                os.rename(filename, video_path)
                break
    return video_path


def reg_href(div):
    start_index = div.find('href="') + len('href="')
    end_index = div.find('"', start_index)
    href_content = div[start_index:end_index]
    return href_content


def parse_response(user_response):
    song_response = user_response.replace(" ", "%20")
    base = "https://mp3party.net"
    baze_url = "https://mp3party.net/search?q=" + song_response
    html = requests.get(baze_url)
    html = html.text
    soup = BeautifulSoup(html, 'html.parser')
    download_links = soup.find_all('div', {"class": "track song-item"})
    print(baze_url)

    for link in download_links:
        for j_line in str(link).split("\n"):
            if j_line.startswith("<a"):
                href_content = reg_href(j_line)
                print(base + href_content)
                result = (get_download_url(base + href_content), user_response)
                print(result[0])
                download_file(url=result[0], filename=result[1] + ".mp3")

        break


def download_file(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        folder = "music"
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename.lower())
        with open(filepath, 'wb') as file:
            file.write(response.content)
        print(f"Файл {filename} успешно скачан в папку {folder}.")
    else:
        print("Не удалось скачать файл.")


def get_download_url(url):
    l_html = requests.get(url)
    l_html = l_html.text
    l_soup = BeautifulSoup(l_html, 'html.parser')
    l_download_link = l_soup.find_all('div', {"id": "download"})
    for div_line in str(l_download_link).split("\n"):
        return reg_href(div_line)


@bot.event
async def on_ready():
    print(f"Музыкальная папка: {music_folder}")
    print(f'Запущен бот: {bot.user.name}')


@bot.command()
async def test1(ctx):
    await ctx.send('Бот работает!')


voice_states = {}


@bot.command(name='join', help='Ща подскочу на канал')
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_states[ctx.guild.id] = await channel.connect()
    else:
        await ctx.send("Вы должны быть подключены к голосовому каналу, чтобы вызвать эту команду.")


@bot.command(name='str_test', help='Ща затестирую')
async def str_test(ctx, *args):
    joined_args = ' '.join(args)
    await ctx.send(f"Вы ввели {joined_args}")


@bot.command(name='test', help='Ща затестирую')
async def test(ctx):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = r"C:\Users\wowbg\PycharmProjects\pythonProject3\muzbot\music\test.mp3"
            song_name = r"test.mp3"
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Сейчас играет:** {}'.format(song_name))
    except AttributeError:
        await join(ctx)
        await test(ctx)


@bot.command(name='play_name', help='Ща затестирую')
async def play_name(ctx, *args):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            user_response = ' '.join(args)
            parse_response(user_response)
            if voice_channel is not None:
                await ctx.send('**Сейчас играет:** {}'.format(user_response))
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",
                                                      source=f"C:\\Users\\wowbg\\PycharmProjects\\pythonProject3\\muzbot\\music\\{user_response}.mp3"))
    except AttributeError:
        await join(ctx)
        await play_name(ctx, *args)


@bot.command()
async def leave(ctx):
    if ctx.guild.id in voice_states:
        voice_client = voice_states[ctx.guild.id]
        await voice_client.disconnect()
        del voice_states[ctx.guild.id]
    else:
        await ctx.send("Бот не подключен к голосовому каналу.")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) and message.attachments:
        for attachment in message.attachments:
            if attachment.filename.endswith('.mp3'):
                folder_path = os.path.join('music', str(message.author))
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                await attachment.save(os.path.join(folder_path, attachment.filename.lower().replace("_", " ")))
                await message.channel.send(f"Трек {attachment.filename} сохранен в папку music/{message.author}")
            else:
                await message.channel.send("Извините, я могу сохранять только файлы в формате MP3")

    await bot.process_commands(message)


@bot.command(name='my_playlist', help='Ща затестирую')
async def my_playlist(ctx):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            if voice_channel is not None:
                await ctx.send('**Сейчас играет плейлист:** {}'.format(ctx.author))
            folder_path = f'C:\\Users\\wowbg\\PycharmProjects\\pythonProject3\\muzbot\\music\\{ctx.author}'
            for root, dirs, files in os.walk(folder_path):
                for file_name in files:
                    if voice_channel is not None:
                        await ctx.send(f'**Сейчас играет:** {file_name[:-4]}')
                    file_path = os.path.join(root, file_name)
                    song = file_path.split("\\")[-1]
                    voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",
                                                              source=f"C:\\Users\\wowbg\\PycharmProjects\\pythonProject3\\muzbot\\music\\{ctx.author}\\{song}"))
                    while voice_channel.is_playing():
                        await asyncio.sleep(1)
    except AttributeError:
        await join(ctx)
        await my_playlist(ctx)


@bot.command(name='play_dir', help='Ща затестирую')
async def play_dir(ctx, *args):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            user_response = ' '.join(args)
            # parse_response(user_response)
            if voice_channel is not None:
                await ctx.send('**Сейчас играет:** {}'.format(user_response))
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe",
                                                      source=f"C:\\Users\\wowbg\\PycharmProjects\\pythonProject3\\muzbot\\music\\{user_response}.mp3"))
    except AttributeError:
        await join(ctx)
        await play_dir(ctx, *args)


@bot.command(name='url', help='Ща затестирую')
async def url(ctx, url):
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client
        if voice_channel is None:
            await join(ctx)
        if voice_channel is not None:
            await ctx.send("**Начинаю загрузку песни**")
        global music_folder
        async with ctx.typing():
            audio_path = download_audio_from_youtube(url, 'music')
            user_response = audio_path.split("\\")[-1]
            if voice_channel is not None:
                await ctx.send('**Сейчас играет:** {}'.format(user_response[:len(user_response)-4]))
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=os.path.join(music_folder,
                                                                                                   str(user_response))))
    except AttributeError:
        await join(ctx)
        await url(ctx, url)
    except FileExistsError:
        async with aiofiles.open('ta_daun.txt', 'r') as file:
            content = await file.read()
            user_response = content.replace(".mp3", "")
            user_response = user_response.split(" ")
        await play_dir(ctx, *user_response)


bot.run(token)
