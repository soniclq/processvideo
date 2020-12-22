


import os
# import ffprobe3
# from ffprobe import FFProbe
from ffprobe3 import FFProbe

### 获得视频文件列表
videoPath = "/home/sonic/musicProject"

def getVideoFileList():
    pass

def getVideoDuration(path):
    matedata = FFProbe(path)
    # print("streams",len(matedata))matedata
    for stream in matedata.streams:
        if stream.is_video():
            print(stream.duration_seconds())

def main():
    videolist = getVideoFileList()

    ### ffmpeg 合并文件
    print ("hello world!!")

    getVideoDuration(videoPath+"/v1.mp4")


main()