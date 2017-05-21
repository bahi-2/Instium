from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time


yourMessage = ""
yourUserName = ""
yourPassword = ""

class driver:
	def __init__(self, webdriver):
		self.webdriver = webdriver
		self.action = TouchAction(webdriver)

def log_in(dr):
	login = dr.webdriver.find_element_by_id("com.instagram.android:id/log_in_button")
	dr.action.tap(login).perform()
	username = dr.webdriver.find_element_by_id("com.instagram.android:id/login_username")
	dr.webdriver.set_value(username, yourUserName)
	password = dr.webdriver.find_element_by_id("com.instagram.android:id/login_password")
	dr.webdriver.set_value(password, yourPassword)
	login = dr.webdriver.find_element_by_id("com.instagram.android:id/next_button")
	dr.action.tap(login).perform()


def open_messages_tab(dr):
	inbox = dr.webdriver.find_element_by_id("com.instagram.android:id/action_bar_inbox_icon_with_badge")
	dr.action.tap(inbox).perform()


def send_message(dr):
	writeField = dr.webdriver.find_element_by_id("com.instagram.android:id/row_thread_composer_edittext")
	writeField.send_keys(yourMessage)
	sendButton = dr.webdriver.find_element_by_id("com.instagram.android:id/row_thread_composer_button_send")
	dr.action.tap(sendButton).perform()
	backButton = dr.webdriver.find_element_by_id("com.instagram.android:id/action_bar_button_back")
	dr.action.tap(backButton).perform()


def respond_to_users(dr):
	messages = dr.webdriver.find_elements_by_id("com.instagram.android:id/row_inbox_digest")
	for message in messages:
		if message.get_attribute('text') != yourMessage:
			dr.action.tap(message).perform()
			send_message(dr)
			break


""" desired_caps are desired Capabilities, they are like prefrences for your virtual machine,
learn more about what you can use at:
https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/caps.md """
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '7.1.1'
desired_caps['deviceName'] = 'Android Simulator'
desired_caps['appActivity'] = '.activity.MainTabActivity'
desired_caps['appPackage'] = 'com.instagram.android'
# desired_caps['newCommandTimeout'] = 0 # needed only for testing purposes, leave commented

try:
	dr = driver(webdriver.Remote('http://localhost:4723/wd/hub', desired_caps))

	print("Session started with id: " + str(dr.webdriver.session_id)) # the session id can be usefull if you 
	# want to attach to the session from appium-desktop

	log_in(dr)
	open_messages_tab(dr)
	while True:
		respond_to_users(dr)
		time.sleep(2)
		
except:
	import traceback
	import sys
	e = sys.exc_info()
	print("Error: %s , %s " % (e[0], e[1]))
	traceback.print_tb(e[2])
	dr.webdriver.quit()
	sys.exit()