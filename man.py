


import os
import subprocess
import platform
import glob
# import ffprobe3
# from ffprobe import FFProbe
from ffprobe3 import FFProbe

### 获得视频文件列表
videoPath = "/home/sonic/musicProject"


def merge_file( file_directory):
    # 路径+“/” + "*.mpt"
    mp4_file_dir = os.path.join(file_directory, "*.mp4")

    # 对路径下的mp4文件名进行排序
    file_name_list = sorted(glob.glob(mp4_file_dir))

    if (len(file_name_list) == 0):
        # self.logger.error(u"[文件目录] {0}".format(file_direcotry))
        raise Exception(u"目录中文件不存在")

    # 遍历文件名列表
    for file_name in file_name_list:
        # 取目录或者文件名
        base_name = os.path.basename(file_name)
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
    merge_file_path = file_directory+"/out.mp4"

    try:
        with open(temp_file_path, 'w') as f2:
            for file_name in file_name_list:
                f2.write("file  " + file_name + "\n")
    except Exception as e:
        raise Exception()

    # mp4 文件合并
    cmd = "ffmpeg -f concat -loglevel error -safe 0 -i " + temp_file_path + " -c copy " + merge_file_path

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
    for stream in matedata.streams:
        if stream.is_video():
            print(stream.duration_seconds())

def main():
    videolist = getVideoFileList()

    ### ffmpeg 合并文件
    print ("hello world!!")
    # concatVideoFiles()
    merge_file(videoPath)

    getVideoDuration(videoPath+"/v1.mp4")


main()