import youtube_dl
from moviepy.editor import *


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
        video_path = os.path.join(output_path, video_title)
        for filename in os.listdir("."):
            if filename.endswith(".mp3"):
                os.rename(filename, video_path)
                break
    return video_path


youtube_url = 'https://www.youtube.com/watch?v=4X7ZvpwBiKA'
output_path = 'music'
print(download_audio_from_youtube(youtube_url, output_path))
