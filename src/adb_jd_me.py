import os, time, random, subprocess
from subprocess import Popen, call


def init_usb_conn():
    call('adb devices', shell=True)
    print('adb devices usb conn....ok')
    time.sleep(1)


def awake_phone():
    adb_console = adb_popen('adb shell dumpsys window policy')
    if 'mShowingLockscreen=false' in adb_console and 'mScreenOnEarly=false' in adb_console:
        call('adb shell input keyevent 26', shell=True)
    print('awake phone....ok')
    time.sleep(1)


def adb_input_shell(s):
    cmd = 'adb shell input %s' % s
    call(cmd, shell=True)
    print('adb shell:%s ....ok' % cmd)
    time.sleep(2)


def adb_move_to(x1: int, y1: int, x2: int, y2: int):
    cmd = 'adb shell input swipe %s %s %s %s ' % (x1, y1, x2, y2)
    call(cmd, shell=True)
    print('%s ....ok' % cmd)
    time.sleep(1)


def adb_long_press(x: int, y: int, press_time=1200):
    cmd = 'adb shell input swipe %s %s %s %s %s' % (x, y, x + 1, y + 1, press_time)
    call(cmd, shell=True)
    print('%s ....ok' % cmd)
    time.sleep(1)


def adb_start_app(app_package: str, app_main_activity: str):
    cmd = 'adb shell am start -n %s/%s.%s' % (app_package, app_package, app_main_activity)
    print(cmd)
    call(cmd, shell=True)
    time.sleep(1)


def adb_stop_app(app_package: str):
    cmd = 'adb shell am force-stop %s' % app_package
    print(cmd)
    call(cmd, shell=True)
    time.sleep(1)


def adb_popen(cmd: str):
    ret_lines = []
    with Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as f1:
        while True:
            buff = f1.stdout.readline()
            ret = Popen.poll(f1)
            line = None
            if buff:
                line = buff.decode(encoding='utf-8').strip('\r\n')
                ret_lines.append(line)
            if ret is not None:
                break
    return '\n'.join(ret_lines)


if __name__ == '__main__':
    init_usb_conn();
    time.sleep(5)
    # 点击领京豆
    while True:
        adb_input_shell('tap 680 370')
        time.sleep(1)
        adb_input_shell('tap 500 370')
        time.sleep(5)
