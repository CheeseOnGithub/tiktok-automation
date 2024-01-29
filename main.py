from __future__ import unicode_literals
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, clips_array
import os
import random
import scrapetube
import pyfiglet
import whisper_timestamped
from tiktok_uploader.upload import upload_video

#only needs to be done once tbh
def getVids():
    videos = scrapetube.get_channel(channel_url="https://www.youtube.com/@MOVIECLIPS")

    with open("videos.txt", "w") as file:
        for vid in videos:
            print("saved video " +  vid["title"]["runs"][0]["text"])
            file.write("https://www.youtube.com/watch?v="+ vid["videoId"] + "\n")


# returns names of videos
def downloadVids(arr):
    ydl_opts = {
        'quiet': True,
        'format': 'best[ext=mp4]'
    }
    names = []
    print("downloading videos :3")
    with YoutubeDL(ydl_opts) as ydl:
        for i in arr:
            info = ydl.extract_info(i, download=False)
            if info["age_limit"] == 18:
                print("video is age restricted grrr")
                subtitles()
            file_path = ydl.prepare_filename(info)
            names.append(os.path.splitext(file_path)[0]+'.mp4')
        ydl.download(arr)

        print("downloaded")

    return names

def createSubtitlesFromClip(clip):
    clip.audio.write_audiofile("audiofromvid.wav", codec='pcm_s16le')
    model = whisper_timestamped.load_model("base")
    results = whisper_timestamped.transcribe(model, "audiofromvid.wav")

    subs = []
    subs.append(clip)
    for segment in results["segments"]:
        for word in segment["words"]:
            text = word["text"]
            start = word["start"]
            end = word["end"]
            duration = end - start
            textClip = TextClip(txt=text, fontsize=60, stroke_width=1, stroke_color="black", color="white")
            textClip = textClip.set_start(start).set_duration(duration).set_pos(("center", "center")).margin(top=350, opacity=0)
            subs.append(textClip)

    os.remove("audiofromvid.wav")

    return CompositeVideoClip(subs)

def ADHDMode():
    line = random.choice(open("videos.txt").read().splitlines())
    print(line + " got picked!!!!")
    videos = downloadVids([line, "https://www.youtube.com/watch?v=9eqvo0uqpTs"])

    clip1 = VideoFileClip(videos[0])
    clip2 = VideoFileClip(videos[1]).without_audio() # the subway surfer video or whatever
    
    randomStart = random.uniform(0, clip2.duration - clip1.duration - 30)

    clip1 = createSubtitlesFromClip(clip1)

    
    cropped_clip1 = clip1.crop(width=480, height=720-70, x_center=clip1.size[0]/2, y_center=clip1.size[1]/2)
    cropped_clip2 = clip2.crop(width=480, height=720, x_center=clip2.size[0]/2, y_center=clip2.size[1]/2)
    
    clip2 = cropped_clip2.subclip(randomStart, randomStart + clip1.duration- 30)
    clip1 = cropped_clip1.subclip(0, clip1.duration-30)

    combined = clips_array([[clip1], [clip2]])
    combined2 = combined.resize((1080, 1920))
    combined2.write_videofile("video.mp4", codec='h264_nvenc')

    upload_video("video.mp4", "#fyp #foryou #movie #movieclips #film #asmr #soapasmr ", "cookies.txt")

    os.remove("video.mp4")
    os.remove(videos[0])


def subtitles():
    line = random.choice(open("videos.txt").read().splitlines())
    print(line + " got picked!!!!")
    videos = downloadVids([line])
    print(videos)
    vidClip = VideoFileClip(videos[0])
    clip = createSubtitlesFromClip(vidClip)
    cropped_clip1 = clip.resize(height=1920)
    cropped_clip1 = cropped_clip1.crop(x1=1166.6,y1=0,x2=2246.6,y2=1920)
    cropped_clip1.subclip(0, cropped_clip1.duration-30)
    cropped_clip1.write_videofile("video.mp4", codec='h264_nvenc')

    upload_video("video.mp4", "#fyp #foryou #movie #movieclips #film ", "cookies.txt")

    os.remove("video.mp4")
    os.remove(videos[0])



if __name__ == "__main__":
    print(pyfiglet.figlet_format("tiktok    brainrot", "big"))
    print("[1] soap mode")
    print("[2] subtitle mode")
    print("[3] get videos (only use once and takes a while)")

    res = input("> ")

    match res:
        case "1":
            inp = input("how many vids u wanna upload: ")
            for i in range(int(inp)):
                ADHDMode()
        case "2":
            inp = input("how many vids u wanna upload: ")
            for i in range(int(inp)):
                subtitles()
        case "3":
            getVids()
        case _:
            print("ur retarded")