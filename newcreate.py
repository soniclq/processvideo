import glob
import os
import subprocess
from datetime import datetime

from ffprobe3 import FFProbe

import Constans

file_list = "/Volumes/SSD/download/music/picture"
ffmpegPath = "/Volumes/SSD/workplace/ffmpeg-opengl/ffmpeg-4.3.1/ffmpeg"

def ffmpeg_run(cmd):
    try:
        proc = subprocess.Popen(cmd, shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        out, err = proc.communicate()
        # for a in iter(proc.stdout.readline, b''):
        #     a = a.decode('UTF-8')
        #     print(a)
    except Exception as e:

        raise Exception()
    finally:
        pass
def getTimeStr():
    return datetime.now().strftime("%m%d%H%M%S")


def getVideoDuration(path):
    matedata = FFProbe(path)
    # print("streams",len(matedata))matedata
    videoDuration = 0
    for stream in matedata.streams:
        if stream.is_video():
            videoDuration = stream.duration_seconds()
    return videoDuration

def getAudioDuration(path):
    matedata = FFProbe(path)
    adur = 0
    for stream in matedata.streams:
        if stream.is_audio():
            adur = stream.duration_seconds()
    return adur

def merge_videoList(videolist):

    merge_file_text = Constans.VIDEOMIDDLEPATH+"/video.text"
    merge_file_output = Constans.VIDEOMIDDLEPATH+"/"+getTimeStr()+".mp4"
    # try:      with
    try:
        with open(merge_file_text, 'w') as f2:
            for file_name in videolist:
                f2.write("file  " + file_name + "\n")
    except Exception as e:
        raise Exception()
    cmd = "ffmpeg -f concat -loglevel error -safe 0 -i " + merge_file_text + " -c copy " + merge_file_output
    ffmpeg_run(cmd)
    return merge_file_output

def merge_audiolist(audioList):

    merge_file_text = Constans.AUDIOFILEROOTPATH+"/audio.txt"
    merge_file_output = Constans.AUDIOFILEROOTPATH+getTimeStr()+".mp3"
    # try:      with
    try:
        with open(merge_file_text, 'w') as f2:
            for file_name in audioList:
                f2.write("file  " + file_name + "\n")
    except Exception as e:
        raise Exception()
    cmd = "ffmpeg -f concat -loglevel error -safe 0 -i " + merge_file_text + " -c copy " + merge_file_output
    ffmpeg_run(cmd)
    return merge_file_output

def main():
    pict_dir = os.path.join(file_list, "*.*")
    file_name_list = sorted(glob.glob(pict_dir))

    outfile = os.getcwd()+"./out.mp4"
    for pic in file_name_list:
        finaloutfile = os.getcwd()+"/" + getTimeStr() + ".mp4"
        cmd = '''%s  -loop 1 -i %s -pix_fmt yuv420p -vcodec libx264 -b:v 600k -r:v 25 -preset medium -crf 29 -vframes 360  -r 18 -t\
         30 -filter_complex "plusglshader=sdsource=snow_shader.gl:vxsource=snow_vertex.gl"  -an -f mp4 -y %s'''  % (ffmpegPath, pic, finaloutfile)
        ffmpeg_run(cmd)
        vdur = getVideoDuration(finaloutfile)

        count = (int)( 2 * 3600 / vdur) + 1
        videolist = []
        cmd = ""
        if ( 2 * 3600 < vdur):
            pass
            # cmd  = "ffmpeg -i %s -ss 0 -t %f -acodec copy %s" % (Constans.AUDIOFILE, vdur ,aoutpath)
        else:
            for i in range(0, count):
                videolist.append(finaloutfile)

        videoOneStepfile = merge_videoList(videolist)
        adur = getAudioDuration(Constans.AUDIOFILE)

        print("audio duration %d" % (adur))
        vdur = getVideoDuration(videoOneStepfile)
        aoutpath = Constans.AUDIO_PREPARE_FILE + getTimeStr()+".mp3"
        count = (int)(vdur / adur) + 1
        audioList = []
        cmd = ""
        if ( vdur < adur):
            cmd  = "ffmpeg -i %s -ss 0 -t %f -acodec copy %s" % (Constans.AUDIOFILE, vdur ,aoutpath)
        else:
            for i in range(0, count):
                audioList.append(Constans.AUDIOFILE)
            temp_audio = merge_audiolist(audioList)

            cmd = "ffmpeg -i %s -ss 0 -t %f -acodec copy %s" % (temp_audio, vdur ,aoutpath)
        print("audio prepare %s......" % cmd)
        ffmpeg_run(cmd)
        print("audio prepare done")
        print("start final video .....")
        finaloutfile = Constans.FINALVIDEOPATH + getTimeStr() + ".mp4"
        ### final merge audio and video
        cmd = 'ffmpeg -i %s -i %s -c copy %s' % (videoOneStepfile, aoutpath, finaloutfile)
        print("start merge audio and video %s" % (cmd))
        try:
            proc = subprocess.Popen(cmd, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)

            out, err = proc.communicate()
            # for a in iter(proc.stdout.readline, b''):
            #     a = a.decode('UTF-8')
            #     print(a)
        except Exception as e:
            raise Exception()
        finally:
            pass
        print("end final video...")
        # break
            # cmd = "ffmpeg -i %s -ss 0 -t %f -acodec copy %s" % (temp_audio, vdur ,aoutpath)




if __name__ == '__main__':
    main()