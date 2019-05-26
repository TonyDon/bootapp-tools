import os, time, logging, random
from appium import webdriver as awd
from subprocess import call

from appium.webdriver import WebElement
from appium.webdriver.common.touch_action import TouchAction

logging.basicConfig(filename=r'C:\export\Logs\jd-bean-robot.log',
                    level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')
logger = logging.getLogger(__file__)


def config_caps():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "64a651e6acec",
        "platformVersion": "4.4.4",
        "noReset": True,
        "autoAcceptAlerts": True,
        "automationName": "Appium",
        "appPackage": "com.jingdong.app.mall",
        "appActivity": "main.MainActivity"
    }
    #desired_caps['app'] = 'app.apk'
    return desired_caps

def init_usb_conn():
    call('adb devices',shell=True)
    logger.info('adb devices usb conn....ok')
    time.sleep(1)

def awake_phone():
    call('adb shell input keyevent 26',shell=True)
    logger.info('awake phone....ok')
    time.sleep(1)

def adb_shell(str):
    cmd = 'adb shell input %s' % str
    call(cmd, shell=True)
    logger.info('adb shell:%s ....ok' % cmd)
    time.sleep(1)

def rand_down_scroll():
    y1 = random.randint(250,280)
    y2 = random.randint(300,350)
    adb_shell('swipe 250 %s 250 %s' % (y1,y2))

def rand_up_scroll():
    y1 = random.randint(240,260)
    y2 = random.randint(200,220)
    adb_shell('swipe 250 %s 250 %s' % (y1,y2))

if __name__ == '__main__' :
    #init_usb_conn()
    ad = awd.Remote('http://127.0.0.1:4723/wd/hub', config_caps())
    logger.info('init appium webdriver!')
    #主页-领京豆区域点击
    box = ad.find_element_by_accessibility_id('OldAppcenter')
    jd_bean = box.find_elements_by_class_name("android.widget.RelativeLayout")[6]
    action = TouchAction(ad)
    action.tap(jd_bean).perform()
    time.sleep(5)
    ayr = ad.find_element_by_id('com.jingdong.app.mall:id/ayr')
    logger.info('ayr %s, %s',ayr.is_displayed(),ayr.location)
    time.sleep(5)
    ayr_sv = ayr.find_element_by_class_name('android.widget.ScrollView')
    logger.info('ayr_sv %s %s',ayr_sv.is_displayed(),ayr_sv.location)
    sign_reach = ayr_sv.find_element_by_xpath('//android.view.View/android.view.View[1]/android.view.View[2]/android.view.View/android.view.View/android.widget.TextView')
    logger.info('sign_reach %s %s',sign_reach.is_displayed(),sign_reach.location)
    action.tap(sign_reach).perform()
    time.sleep(5)
    #种豆
    seed_bean_sv = ad.find_element_by_class_name('android.widget.ScrollView')
    logger.info('seed_bean_sv %s, %s',seed_bean_sv.is_displayed(),seed_bean_sv.location)
    seed_bean_text = seed_bean_sv.find_element_by_xpath('//android.view.View/android.view.View[2]/android.view.View/android.widget.TextView')
    logger.info('seed_bean_text %s, %s',seed_bean_text.is_displayed(),seed_bean_text.location)
    action.tap(seed_bean_text).perform()
    time.sleep(6)
    # 庄园
    garden_ayr = ad.find_element_by_id('com.jingdong.app.mall:id/ayr')
    garden = garden_ayr.find_element_by_xpath('//android.widget.FrameLayout/android.view.View/android.view.View/android.view.View/android.view.View[1]/android.view.View')

    # 拿水瓶
    take_water = None
    try:
        take_water = garden.find_element_by_xpath('//android.view.View[4]/android.view.View[1]/android.view.View[1]/android.widget.ImageView')
        logger.info('garden take water %s %s', take_water.is_displayed(), take_water.location)
        time.sleep(1)
        action.tap(take_water).perform()
    except :
        logger.error('garden take water error. maybe not find water bottle!')

    try_times = 3
    while True:
        try_times=try_times-1
        if try_times == 0 :
            break;
        # 狂会场
        try:
            market = garden.find_element_by_xpath('//android.view.View[8]/android.view.View[4]/android.widget.ImageView')
            logger.info('goto market %s, %s',market.is_displayed(),market.location)
            action.tap(market).perform()
            action.wait(2000)
            time.sleep(10)
            adb_shell('swipe 100 600 100 300')
            time.sleep(5)
            break
        except :
            logger.error('goto market error. maybe not jump market activity!')
            # 返回上一个页面 重新进入会场
            ad.press_keycode(4)
            time.sleep(5)
            action.tap(seed_bean_text).perform()
            time.sleep(5)

    #返回花园
    ad.press_keycode(4)

    # 浇水
    time.sleep(2)
    watering = garden.find_element_by_xpath('//android.view.View[9]/android.view.View/android.view.View/android.widget.ImageView[1]')
    logger.info('garden watering %s %s', watering.is_displayed(), watering.location)
    action.tap(watering).perform()
    time.sleep(1)

    #返回到领京豆页面
    ad.press_keycode(4)
    time.sleep(1)
    ad.press_keycode(4)
    time.sleep(1)

    #end



