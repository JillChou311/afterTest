#coding=utf-8
import os
import unittest
from selenium import webdriver
from appium import webdriver
import page
from time import sleep
from selenium.common.exceptions import WebDriverException


PATH = lambda p: os.path.abspath(
    os.path.join(os.path.dirname(__file__), p)
)


class LiteNet_test(unittest.TestCase):
    """A sample test class to show how page object works"""

    def _ScanSSID(self, ssid, button_id, start_y, end_y):
        scan_result = False
        ssid_elem = None
        for i in range(10):
            elem = self.driver.find_elements_by_id(button_id)
            for e in elem:
                if e.text == ssid:
                    scan_result = True
                    ssid_elem = e
                    break
            if scan_result:
                break
            else:
                self.driver.swipe(200, start_y , 200, end_y, 3000)
        ssid_elem.click()


    def setUp(self):
        sleep(30)
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        for f in files:
            if f[0:17]=='app-Litenet-debug':
                print f
                apkname = f
                
        desired_caps = {}
        desired_caps['app'] = PATH(apkname)
        desired_caps['appPackage'] = 'com.gemteks.litenet'
        desired_caps['appActivity'] = 'com.joymaster.mycasa.activity.MainActivity'
        desired_caps['platformName'] = 'Android'
        # desired_caps['platformVersion'] = '5.0'
        # desired_caps['deviceName'] = 'E9AZCY15Z724'
        # desired_caps['udid'] = 'E9AZCY15Z724'
        desired_caps['platformVersion'] = '4.4.2'
        desired_caps['deviceName'] = 'EAAZCY17E701'
        desired_caps['udid'] = 'EAAZCY17E701'
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.driver.implicitly_wait(30)

    def test_0_wifi_set(self):
        self.driver.quit()

        os.system('adb -s EAAZCY17E701 shell am start -n io.appium.settings/.Settings -e wifi on')

        # sleep(50)

        desired_caps = {
            'platformName': 'Android',
            'platformVersion': '4.4.2',
            'deviceName': 'EAAZCY17E701',
            'appPackage': 'com.android.settings',
            'appActivity': 'Settings'
        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        elem = self.driver.find_elements_by_id("android:id/title")
        for e in elem:
            if e.text == u"Wi‑Fi":
                e.click()
                sleep(2)
                break

        self._ScanSSID("MyVITA_906E", 'android:id/title', 1000, 200)

        elem = self.driver.find_elements_by_class_name("android.widget.Button")
        for e in elem:
            if e.text == u'完成':
                e.click()
                break
            elif e.text == u'連線':
                e.click()
                break


    def test_1_1_register(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.swipe_to_botton()
        login_page.click_regist_button()

        register_page = page.RegisterPage(self.driver)

        #account test case : 234/ 1@gmail.com / 23@gmail.com
        register_page.send_account('234')
        assert register_page.check_error_message(u'信箱格式錯誤'),'error message error.'
        register_page.send_account('1@gmail.com')
        assert register_page.check_error_message(u'該信箱已註冊, 輸入密碼直接登入'),'message error.'
        register_page.send_account('23@gmail.com')
        assert register_page.check_error_message(u'該信箱尚未啟用, 輸入密碼直接註冊'),'message error.'

        #password test case: 234/ 12345678910123456
        register_page.send_password('234')
        assert register_page.check_error_message(u'密碼長度 < 8'),'error message error.'
        register_page.send_password('12345678910123456')
        assert register_page.check_error_message(u'密碼長度 > 15'),'error message error.'

        #passwordconfirm : 1234567891012345(123)
        register_page.send_password('123456789101234')
        register_page.send_password_confirm('123')
        assert register_page.check_error_message(u'密碼與確認密碼不同'),'error message error.'


    def test_1_2_login(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.send_account_info('litnet@gmail.com', '12345678')

        bottom_banner = page.BottomBanner(self.driver)
        bottom_banner.click_bottom_button('設定')

        setting_page = page.SettingPage(self.driver)
        assert setting_page.check_login_name(u'litnet@gmail.com'), 'login fail'



    def test_2_region(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.send_account_info('litnet@gmail.com', '12345678')
        security_page = page.SecurityPage(self.driver)
        assert security_page.check_security_logo_appear(),'security logo not appear.'
        #add new region test
        bottom_banner = page.BottomBanner(self.driver)
        bottom_banner.click_bottom_button('區域')
        region_page = page.RegionPage(self.driver)
        region_page.add_new_region('AutoTest')
        assert region_page.check_out_region('AutoTest'), "Add region fail."

        #edit region test
        region_page.edit_region('AutoTest','AutoTest01')
        assert region_page.check_out_region('AutoTest01'), "Edit region fail."

        #delete region test
        region_page.delete_region('AutoTest01')
        theResult = False
        if region_page.check_out_region('AutoTest01') == False:
            theResult = True
        assert theResult,"delete region fail."



    def test_4_repeat_binding(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.send_account_info('1@gmail.com', '12345678')
        security_page = page.SecurityPage(self.driver)


        security_page = page.SecurityPage(self.driver)
        binding_page = page.BindingPage(self.driver)
        bottom_banner = page.BottomBanner(self.driver)
        setting_page = page.SettingPage(self.driver)

        security_page = page.SecurityPage(self.driver)
        if security_page.check_security_logo_appear() == False:
            binding_page.send_binding_info('906e','59725388','f835ddf7906e')
            binding_page.click_send_button()
            assert security_page.check_security_logo_appear(),'security logo not appear.'

        testTimes = 3 # repeat times is here
        while testTimes > 0:
            bottom_banner.click_bottom_button('設定')
            setting_page.unbinding_device()
            login_page.click_send_button()

            binding_page.send_binding_info('906e','59725388','f835ddf7906e')
            binding_page.click_send_button()
            assert security_page.check_security_logo_appear(),'security logo not appear.'

            testTimes = testTimes-1

    def test_3_scene(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.send_account_info('litnet@gmail.com', '12345678')

        security_page = page.SecurityPage(self.driver)
        assert security_page.check_security_logo_appear(),'security not appear.'

        bottom_banner = page.BottomBanner(self.driver)
        bottom_banner.click_bottom_button('情境')

        scene_page = page.ScenePage(self.driver)
        scene_page.add_new_scene("AutoTest")
        bottom_banner.click_bottom_button('設定')
        bottom_banner.click_bottom_button('情境')
        assert scene_page.check_out_scene('AutoTest'), "Add scene fail."



        scene_page.edit_scene("AutoTest",'AutoTest01')
        bottom_banner.click_bottom_button('設定')
        bottom_banner.click_bottom_button('情境')
        assert scene_page.check_out_scene('AutoTest01'), "Edit scene fail."

        scene_page.delete_scene('AutoTest01')
        #delete region test
        theResult = False
        if scene_page.check_out_scene('AutoTest01') == False:
            theResult = True
        assert theResult,"delete region fail."





    def test_5_logout(self):
        welcome_page = page.WelcomePage(self.driver)
        welcome_page.click_x_button()

        login_page = page.LoginPage(self.driver)
        login_page.send_account_info('litnet@gmail.com', '12345678')

        bottom_banner = page.BottomBanner(self.driver)
        bottom_banner.click_bottom_button('設定')

        setting_page = page.SettingPage(self.driver)

        assert setting_page.check_login_name(u'litnet@gmail.com'), 'login fail'

        setting_page.logout()
        assert login_page.check_Litenet_logo(),'logout fail.'
        self.driver.remove_app('com.gemteks.litenet')






    def tearDown(self):
        self.driver.quit()

if __name__== '__main__' :
    suite = unittest.TestLoader().loadTestsFromTestCase(LiteNet_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
