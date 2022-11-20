import os
import random
import string
from datetime import datetime

import m3u8

'''
Array.prototype.map.call(this.decryptkey, x => ('00' +
x.toString(16)).slice(-2)).join('')
'''

video_link = input("Input m3u8 video link: ")
audio_link = input("Input m3u8 audio link: ")
encryption_key = input("Input the key: ")

current_time = datetime.now().strftime("%H:%M:%S")
video_iv = ""
def compress_m3u8(link, is_audio):
    global video_iv
    playlist = m3u8.load(link)
    ts_len = len(playlist.segments)

    root_video_link = "/".join(link.split("/")[:-1])+"/"
    for i in range(0, ts_len):
        segments = str(playlist.segments[i]).split(",")
        video_iv = segments[2].replace("IV=0x", "").split("\n")[0]
        ts_file = segments[3].replace("\n", "")
        
        if not is_audio:
            os.system("wget "+root_video_link+ts_file+" -O ->> "+current_time+".ts")
        else:
            os.system("wget "+root_video_link+ts_file+" -O ->> "+current_time+"_audio.ts")

def decrypt_ts(filename, is_audio):
    if not is_audio:
        os.system("openssl enc -aes-128-cbc -nosalt -d -in "+filename+".ts -K '"+encryption_key+"' -iv '"+video_iv+"' > decrypted.mkv")
    else:
        os.system("openssl enc -aes-128-cbc -nosalt -d -in "+filename+".ts -K '"+encryption_key+"' -iv '"+video_iv+"' > decrypted.aac")

def combine(filename):
    os.system("ffmpeg -i "+filename+".mkv -i "+filename+".aac -c copy "+''.join(random.choices(string.ascii_uppercase + string.digits, k=6))+".mp4")
    os.system("rm "+filename+".mkv")
    os.system("rm "+filename+".aac")
    os.system("rm "+current_time+".ts")
    os.system("rm "+current_time+"_audio.ts")

compress_m3u8(video_link, False)
decrypt_ts(current_time, False)

if audio_link:
    compress_m3u8(audio_link, True)
    decrypt_ts(current_time+"_audio", True)
    combine("decrypted")




