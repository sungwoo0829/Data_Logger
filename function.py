import discord
from PIL import Image
import ffmpeg
import requests
import io
import moviepy.editor as mp
import os
import sys



async def compression(attach,size):
    info = requests.head(attach.proxy_url)
    type = attach.content_type.split('/')
    data = io.BytesIO(await attach.read())
    if type[0]=="image": 
        return compress_image(data,size,attach)
    elif type[0]=="video":
        return compress_video_output(attach,size)
        

def compress_image(data, size, attach):
    output=io.BytesIO()
    size1=sys.getsizeof(data)
    pro=size1/(size*1000000)
    with Image.open(data) as im:
        if im.is_animated:
            clip=mp.VideoFileClip(attach.proxy_url)
            clip.write_videofile("output.mp4",audio=False)
            with open("output.mp4","rb") as f:
                output = io.BytesIO(f.read())
            output=output.getvalue()
            os.remove("output.mp4")
            name="".join(attach.filename.split(".")[:-1])+".mp4"
            return output, name
        else:
            im=im.convert("RGB")
            if pro<=2:
                im.save(output,format='JPEG', quality=100)
                output=output.getvalue()
                return output
            elif pro<=7:
                im.save(output,format='JPEG', quality=90)
                output=output.getvalue()
                return output
            else:
                im.save(output,format='JPEG', quality=50)
                output=output.getvalue()
                return output, attach.filename
    
        
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

def compress_video_output(attach, size):
    attach.save("input.mp4")

    
    compress_video("input.mp4", 'output.mp4', size * 1000)
    with open("output.mp4","rb") as f:
        output = io.BytesIO(f.read())
    output=output.getvalue()
    os.remove("output.mp4")
    os.remove("input.mp4")
    name="".join(attach.filename.split(".")[:-1])+".mp4"
    return output, name
    