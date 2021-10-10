import json
import os
import random
import subprocess
import platform
import glob
# import ffprobe3
# from ffprobe import FFProbe
import time
from datetime import datetime

from ffprobe3 import FFProbe

### 获得视频文件列表
import Constans
from probe import ffprobe


# videomiddlePath = "/home/sonic/musicProject/middlevideo"
# videoOutpath = "/home/sonic/workplace/bbeProject/out"
# mergeVideo1 = "/home/sonic/workplace/youtubeProject/out/out."
# audiofile = "/home/sonic/musicProject/originaudio/deepsleephealing.mp3"
# audioFileRoot = "/home/sonic/musicProject/"
# prepareVideoPath = "/home/sonic/musicProject/originvideo"
# transcodepath = "/home/sonic/musicProject/transcodevideo"


# headvideoList = [transcodepath+"/0416003741.mp4", transcodepath+"/"
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



def merge_file( file_directory):
    # 路径+“/” + "*.mpt"
    mp4_file_dir = os.path.join(file_directory, "*.mp4")

    # 对路径下的mp4文件名进行排序
    file_name_list = sorted(glob.glob(mp4_file_dir))
    random.shuffle(file_name_list)

    if (len(file_name_list) == 0):
        # self.logger.error(u"[文件目录] {0}".format(file_direcotry))
        raise Exception(u"目录中文件不存在")

    # 遍历文件名列表
    for file_name in file_name_list:
        ffprobe_result = ffprobe(file_name)
        # 取目录或者文件名
        base_name = os.path.basename(file_name)
        if (ffprobe_result.return_code == 0):
            d = json.loads(ffprobe_result.json)
            streams = d.get("streams", [])
            for stream in streams:
                if stream.get("codec_type") == "video":
                    # print(int(eval(stream.get("r_frame_rate")))) =
                    frame_rate = int(eval(stream.get('r_frame_rate')))
                    print (frame_rate)
                    # if frame_rate != 29:
                    #     file_name_list.remove(file_name)

                # print (stream.get("codec_type"))
        # file_name  是文件的场合
        if (os.path.isfile(file_name)):
            # pass
            ###如果文件名中只包含一个"_"
            # if base_name.find()find
            if (base_name[base_name.find("_") + 1:].find("_") > 0):
            #     # 如果该当文件存在的场合
                if os.path.exists(file_name):
                #     # 删除该文件
                #         os.remove(file_name)
                # # file_name_list中移除该文件名
                    file_name_list.remove(file_name)
        else:
        # 不是文件的场合
            file_name_list.remove(file_name)
    first_file_name = file_name_list[0]
    temp_file_path = first_file_name[0:first_file_name.rfind("_")] + ".txt"
    # merge_file_path = first_file_name[0:first_file_name.rfind("/")] + "out.mp4";
    merge_file_path = Constans.VIDEOOUTPUTPATH+"/vout"+getTimeStr()+".mp4"
    print("total %d file" % (len(file_name_list)))
    count = 0
    try:
        with open(temp_file_path, 'w') as f2:
            for count in range(0, 1):
                for file_name in file_name_list:
                    f2.write("file  " + file_name + "\n")
                    # count = count +1
                count = count + 1
                # f2.write("file  " + file_name + "\n")
    except Exception as e:
        raise Exception()

    # mp4 文件合并

    cmd = "ffmpeg -f concat -loglevel error -safe 0 -i " + temp_file_path + " -c copy " + merge_file_path
    print("merge mp4 file now..."+cmd)
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
        if os.path.exists(temp_file_path):
            pass
    return merge_file_path
            # os.remove(temp_file_path)

def concatVideoFiles():
    try:
        with open(os.devnull, 'w') as tempf:
            subprocess.check_call(["ffmpeg", "-h"], stdout=tempf, stderr=tempf)
    except:
        raise IOError('ffmpeg not found.')

    if str(platform.system()) == 'Windows':
        cmd = ["ffprobe", "-show_streams", path]
    else:
        cmd = ["ffmpeg -f concat -safe 0 -i /home/sonic/musicProject/1.txt -c copy output.mp4"]
    cmdline = "ffmpeg -f concat -safe 0 -i /home/sonic/musicProject/1.txt -c copy output.mp4"
    os.system(cmdline)
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # print(p.stdout.readline)
    # for a in iter(p.stdout.readline, b''):
    #     a = a.decode('UTF-8')
    #     print(a)
    # pass


def getVideoFileList():
    pass

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
            # print(stream.duration_seconds())

def getTimeStr():
    return datetime.now().strftime("%m%d%H%M%S")
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
def prepare(file_directory, outpath):
    mp4_file_dir = os.path.join(file_directory, "*.mp4")

    # 对路径下的mp4文件名进行排序
    file_name_list = sorted(glob.glob(mp4_file_dir))

    # out =
    if (len(file_name_list) == 0):
        # self.logger.error(u"[文件目录] {0}".format(file_direcotry))
        raise Exception(u"目录中文件不存在")
    num = 0
    folder = os.path.exists(outpath)
    if not folder:
        os.mkdir(outpath)
    else:
        pass
    for file in file_name_list:
        cmd = "ffmpeg -i %s -map 0:0 -vcodec copy %s/%s-%d.mp4" % (file, outpath, getTimeStr(), num)
        num = num + 1
        print("prepareVideo ffcmd "+cmd)
        ffmpeg_run(cmd)


def encodeVideos(vpath, outpath):
    mp4_file_dir = os.path.join(vpath, "*.mp4")
    folder = os.path.exists(outpath)
    if not folder:
        os.mkdir(outpath)
    else:
        pass
    # 对路径下的mp4文件名进行排序
    file_name_list = sorted(glob.glob(mp4_file_dir))
    for file in file_name_list:
        cmd = "ffmpeg -i %s -c:v libx264 -preset slow -crf 23 -r 25  %s/%s.mp4" % (file, outpath, getTimeStr())
        print (cmd)
        ffmpeg_run(cmd)
        time.sleep(10)


def create_finalvideo():
    ##emove audio channel and put in middle path
    print("prepare video path is "+Constans.PREPAREVIDEOPATH+"......")
    # prepare(prepareVideoPath)
    print("prepare done")

    ## encode video
    # encodeVideos(videomiddlePath)

    vdur = 0
    videolist = getVideoFileList()

    ### ffmpeg 合并文件
    # concatVideoFiles()
    outfile = merge_file(Constans.TRANSCODEVIDEOPATH)
    print ("merge_file done")
    # ffprobe_result = ffprobe(file_path=videoPath))


    # getVideoDuration(videoPath+"/v1.mp4")
    vdur = getVideoDuration(outfile)
    print("video duration %d" % (vdur))
    adur = getAudioDuration(Constans.AUDIOFILE)

    print("audio duration %d" % (adur))
    aoutpath = "/home/sonic/musicProject/aout" + getTimeStr()+".mp3"
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
    cmd = 'ffmpeg -i %s -i %s -c copy %s' % (outfile, aoutpath, finaloutfile)
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

    if os.path.exists(outfile):
        os.remove(outfile)
    print("end final video...")


def reencodeFile():
    prepare(Constans.ENCODEPATH, Constans.ENCODEPATHOUT)
    encodeVideos(Constans.ENCODEPATHOUT, Constans.ENCODEOUTPATH)

# reencodeFile()

i = 2
for a in range(0, i):
    create_finalvideo()




# encodeVideos()

