import discord
from PIL import Image, ImageSequence
import ffmpeg
import requests
import io
import moviepy.editor as mp
import os


async def compression(attach,size):
    info = requests.head(attach.proxy_url)
    size1=int(info.headers["Content-Length"])
    type = attach.content_type.split('/')
    pro=size1/(size*1000000)
    da = io.BytesIO(await attach.read())
    if type[0]=="image":
        data=io.BytesIO()
        with Image.open(da) as im:
            if im.is_animated:
                clip=mp.VideoFileClip(da)
                clip.write_videofile(data,audio=False)
                data=data.getvalue()
                return data
            else:
                if pro<=2:
                    im.save(data,format='JPEG', quality=100)
                    data=data.getvalue()
                    return data
                elif pro<=7:
                    im.save(data,format='JPEG', quality=90)
                    data=data.getvalue()
                    return data
                else:
                    im.save(data,format='JPEG', quality=50)
                    data=data.getvalue()
                    return data
        
def compress_video(video_full_path, output_file_name, target_size):
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32000
    max_audio_bitrate = 256000

    probe = ffmpeg.probe(video_full_path)
    # Video duration, in s.
    duration = float(probe['format']['duration'])
    # Audio bitrate, in bps.
    audio_bitrate = float(next((s for s in probe['streams'] if s['codec_type'] == 'audio'), None)['bit_rate'])
    # Target total bitrate, in bps.
    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    # Target audio bitrate, in bps
    if 10 * audio_bitrate > target_total_bitrate:
        audio_bitrate = target_total_bitrate / 10
        if audio_bitrate < min_audio_bitrate < target_total_bitrate:
            audio_bitrate = min_audio_bitrate
        elif audio_bitrate > max_audio_bitrate:
            audio_bitrate = max_audio_bitrate
    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    i = ffmpeg.input(video_full_path)
    ffmpeg.output(i, os.devnull,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 1, 'f': 'mp4'}
                  ).overwrite_output().run()
    ffmpeg.output(i, output_file_name,
                  **{'c:v': 'libx264', 'b:v': video_bitrate, 'pass': 2, 'c:a': 'aac', 'b:a': audio_bitrate}
                  ).overwrite_output().run()

    