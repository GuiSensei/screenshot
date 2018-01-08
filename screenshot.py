#!/usr/bin/env python
"""
手机屏幕截图
1. 安卓手机，打开开发者模式，并开启USB调试模式
2. 需要安装adb，adb驱动下载地址：https://adb.clockworkmod.com/
3. 需要安装pillow模块
"""

import time
import subprocess
import os
import sys
from PIL import Image

def dump_device_info():
    """
    显示设备信息
    """
    size_str = os.popen('adb shell wm size').read()
    device_str = os.popen('adb shell getprop ro.product.device').read()
    phone_os_str = os.popen('adb shell getprop ro.build.version.release').read()
    density_str = os.popen('adb shell wm density').read()
    print("""**********
设备信息：
Screen: {size}
Density: {dpi}
Device: {device}
Phone OS: {phone_os}
Host OS: {host_os}
Python: {python}
**********\n""".format(
        size=size_str.strip(),
        dpi=density_str.strip(),
        device=device_str.strip(),
        phone_os=phone_os_str.strip(),
        host_os=sys.platform,
        python=sys.version
    ))

def screenshot(i): #参数i是为了图片后缀不同，否则新图会覆盖旧图
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    if os.path.isfile('picture({}).png'.format(i)):
        try:
            os.remove('picture({}).png'.format(i))
        except Exception:
            pass        
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen('adb shell screencap -p',shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        f = open('picture({}).png'.format(i), 'wb')
        f.write(binary_screenshot)
        f.close()
    elif SCREENSHOT_WAY == 0:
        os.system('adb shell screencap -p /sdcard/picture({}).png'.format(i))
        os.system('adb pull /sdcard/picture({}).png .'.format(i))

def check_screenshot(i):
    global SCREENSHOT_WAY      
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备')
        sys.exit()
    screenshot(i)
    try:
        Image.open('./picture({}).png'.format(i)).load()
        print(time.strftime('%H:%M:%S')+' 采用方式 {} 截取picture({}).png  按Ctrl+C停止程序'.format(SCREENSHOT_WAY,i))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot(i)

def directory():#创建带时间戳的文件夹
    timestamp = time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))
    if not os.path.isdir(timestamp):
        try:
            os.mkdir(timestamp)#创建目录
        except Exception:
            pass     
    os.chdir(os.getcwd()+'/'+timestamp)#改变工作目录到新建的目录下
         
if __name__ == "__main__":    
    SCREENSHOT_WAY = 3  #SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
    #dump_device_info()  #设备信息
    directory()         #创建文件夹
    i = 1               #图片后缀
    while True:
        try:
            check_screenshot(i)
            i += 1
            #time.sleep(1) #设置时间间隔截图（有时截图太快来不及显示就被删除了）
        except KeyboardInterrupt:
            print('程序停止')
            break
