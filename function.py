import discord
from PIL import Image
import requests
import io
import moviepy.editor as mp
import os
import sys



async def compression(attach,size):
    type = attach.content_type.split('/')
    data = io.BytesIO(await attach.read())
    if type[0]=="image": 
        return compress_image(data,size,attach)
    elif type[0]=="video":
        return compress_video(attach,size)
    elif type[0]=="audio":
        return compress_audio(attach,size)
        

def compress_image(data, size, attach):
    output=io.BytesIO()
    size1=sys.getsizeof(data)
    pro=size1/(size*1000000)
    with Image.open(data) as im:
        if im.is_animated:
            prefix=str(attach.id)
            clip=mp.VideoFileClip(attach.proxy_url)
            clip.write_videofile(prefix+"output.mp4",audio=False)
            clip.close()
            with open(prefix+"output.mp4","rb") as f:
                output = io.BytesIO(f.read())
            output=output.getvalue()
            os.remove(prefix+"output.mp4")
            name="".join(attach.filename.split(".")[:-1])+".mp4"
            return output, name
        else:
            im=im.convert("RGB")
            if pro<=2:
                im.save(output,format='JPEG', quality=100)
                output=output.getvalue()
                return output, attach.filename
            elif pro<=7:
                im.save(output,format='JPEG', quality=90)
                output=output.getvalue()
                return output, attach.filename
            else:
                im.save(output,format='JPEG', quality=50)
                output=output.getvalue()
                return output, attach.filename
    
        
def compress_video(attach, target_size):
    output=io.BytesIO()
    prefix=str(attach.id)
    # Reference: https://en.wikipedia.org/wiki/Bit_rate#Encoding_bit_rate
    min_audio_bitrate = 32
    max_audio_bitrate = 256

    clip=mp.VideoFileClip(attach.proxy_url)

    duration = clip.duration

    target_total_bitrate = (target_size * 1024 * 8) / (1.073741824 * duration)

    info = requests.head(attach.proxy_url)
    pro=int(info.headers["Content-Length"])/target_size*1024*1024

    if 256/pro>max_audio_bitrate:
        audio_bitrate=max_audio_bitrate
    elif 256/pro<min_audio_bitrate:
        audio_bitrate=min_audio_bitrate
    else:
        audio_bitrate=int(256/pro)

    # Target video bitrate, in bps.
    video_bitrate = target_total_bitrate - audio_bitrate

    clip.write_videofile(filename=prefix+"output.mp4",bitrate=str(video_bitrate)+"k",audio_bitrate=str(audio_bitrate)+"k")
    clip.close()
    with open(prefix+"output.mp4","rb") as f:
        output = io.BytesIO(f.read())
    output=output.getvalue()
    os.remove(prefix+"output.mp4")
    name="".join(attach.filename.split(".")[:-1])+".mp4"
    return output, name

def compress_audio(attach, size):
    prefix=str(attach.id)
    audioclip=mp.AudioFileClip(attach.proxy_url)
    duration = audioclip.duration
    clip=mp.ImageClip("test.png",duration=duration)
    clip.audio=audioclip
    bitrate = (size * 1000 * 8) / (1.073741824 * duration)
    clip.write_videofile(prefix+"output.mp4",fps=1,audio_bitrate=str(int(bitrate))+"k")
    clip.close()
    audioclip.close()
    with open(prefix+"output.mp4","rb") as f:
        output = io.BytesIO(f.read())
    output=output.getvalue()
    os.remove(prefix+"output.mp4")
    name="".join(attach.filename.split(".")[:-1])+".mp4"
    return output, name
