import os, time, random, subprocess
from subprocess import Popen,call

def init_usb_conn():
    call('adb devices',shell=True)
    print('adb devices usb conn....ok')
    time.sleep(1)

def awake_phone():
    adb_console = adb_popen('adb shell dumpsys window policy')
    if 'mShowingLockscreen=false' in adb_console and 'mScreenOnEarly=false' in adb_console:
        call('adb shell input keyevent 26',shell=True)
    print('awake phone....ok')
    time.sleep(1)

def adb_input_shell(s):
    cmd = 'adb shell input %s' % s
    call(cmd, shell=True)
    print('adb shell:%s ....ok' % cmd)
    time.sleep(2)

def adb_move_to(x1:int,y1:int, x2:int, y2:int):
    cmd = 'adb shell input swipe %s %s %s %s ' % (x1,y1,x2,y2)
    call(cmd, shell=True)
    print('%s ....ok' % cmd)
    time.sleep(1)
    
def adb_long_press(x:int,y:int, press_time = 800):
    cmd = 'adb shell input swipe %s %s %s %s %s' % (x,y,x+1,y+1,press_time)
    call(cmd, shell=True)
    print('%s ....ok' % cmd)
    time.sleep(1)

def adb_start_app(app_package:str, app_main_activity:str):
    cmd = 'adb shell am start -n %s/%s.%s' % (app_package, app_package,app_main_activity)
    print(cmd)
    call(cmd, shell=True)
    time.sleep(1)

def adb_stop_app(app_package:str):
    cmd = 'adb shell am force-stop %s' % app_package
    print(cmd)
    call(cmd, shell=True)
    time.sleep(1)

def adb_popen(cmd:str):
    ret_lines = []
    with Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as f1:
        while True:
            buff = f1.stdout.readline()
            ret = Popen.poll(f1)
            line = None
            if buff :
                line = buff.decode(encoding='utf-8').strip('\r\n')
                ret_lines.append(line)
            if  ret is not None:
                break
    return '\n'.join(ret_lines)

if __name__ == '__main__' :
    init_usb_conn();
    awake_phone();
    adb_start_app('com.jingdong.app.mall','main.MainActivity')
    time.sleep(8)
    # 点击领京豆
    adb_input_shell('tap 200 700')
    time.sleep(5)
    # 点击签到
    adb_input_shell('tap 320 250')
    time.sleep(3)
    # 点击种瓜分豆
    adb_input_shell('tap 320 340')
    time.sleep(4)
    # 点击农场营养液
    adb_input_shell('tap 150 650')
    # 点击逛会场
    adb_input_shell('tap 580 1100')
    time.sleep(3)
    # 会场里 模拟上下滑动
    adb_move_to(200,800, 200, 300)
    #adb_long_press(200,320)
    adb_move_to(200,300, 200, 500)
    #返回到农场
    adb_input_shell('keyevent 4')
    time.sleep(2)
    # 点击浇水
    adb_input_shell('tap 250 950')
    time.sleep(2)
    # 返回上一页
    adb_input_shell('keyevent 4')
    adb_input_shell('keyevent 4')

    adb_stop_app('com.jingdong.app.mall')

