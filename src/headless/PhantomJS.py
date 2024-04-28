#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import ui as ui
from selenium.webdriver.support import expected_conditions as EC


def run(url):
  try:
    # 執行檔的路徑 webdriver
    options = webdriver.FirefoxOptions()
    options.binary_location = 'D:/Application/Browser/Firefox-78/firefox.exe'
    # 设置首选项 (preferences)
    options.set_preference("webdriver.gecko.driver", "D:/Application/Browser/webdriver/geckodriver.exe")
    # 设置 headless 模式
    # options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)
    # 安装扩展程序 (addons)  可选，替换为扩展程序路径
    # browser.install_addon("D:/Application/Browser/webdriver/selenium_ide-3.17.4.xpi")

    browser.get(url)
    # assert 'Yahoo' in browser.title

    print(browser.title)

    # elem = browser.find_element(By.NAME, 'p')  # Find the search box
    # elem.send_keys('seleniumhq' + Keys.RETURN)
    items = browser.find_element(By.XPATH,  "//div[@class='content-layout__item__SC_GG']")

    print(items.text)
    # 等待搜索结果加载
    # browser.implicitly_wait(10)

    # 关闭浏览器
    # browser.quit()
  except:
    traceback.print_exc()
  finally:
    pass
    # driver.quit()
    # service.stop()


if __name__ == '__main__':
  run('https://www.reuters.com/markets/companies/5401.T')




