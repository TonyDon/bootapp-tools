import os, time
from subprocess import call, Popen

call('adb shell input tap 200 690',shell=True)
time.sleep(5)
call('adb shell input tap 650 200',shell=True)
time.sleep(5)
call('adb shell input tap 300 980',shell=True)
time.sleep(1)
call('adb shell input swipe 250 250 300 300',shell=True)
time.sleep(1)
call('adb shell input keyevent 4',shell=True)
time.sleep(2)
call('adb shell input keyevent 4',shell=True)
time.sleep(1)
screem_img = 'adb-screen-%s.png' % int(time.time()*1000)
call('adb shell screencap -p /sdcard/%s' % screem_img, shell=True)
time.sleep(1)
call('adb pull /sdcard/%s C:/tmpdir' % screem_img, shell=True)
time.sleep(1)
out_img = r'C:\tmpdir\%s' % screem_img
print(out_img, os.path.exists(out_img))