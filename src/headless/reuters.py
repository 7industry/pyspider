#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import traceback

from selenium import webdriver
from selenium.webdriver.common.by import By

from api import database
from model.SchemaModel import EquityProfile


class Reuters:

  @classmethod
  def update_equity_statistics(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()

    mapping = {
      'Dividend Yield': 'dividend_yield',
      'P/E Excl. Extra Items (TTM)': 'per',
      'Total Debt/Total Equity (Quarterly)': 'debt_equity_ratio',
      'Return On Equity (TTM)': 'roe',
    }

    try:
      # 執行檔的路徑 webdriver
      options = webdriver.FirefoxOptions()
      options.binary_location = 'D:/Application/Browser/Firefox-78/firefox.exe'
      # 设置首选项 (preferences)
      options.set_preference("webdriver.gecko.driver", "D:/Application/Browser/webdriver/geckodriver.exe")
      # 设置 headless 模式
      options.add_argument('--headless')

      driver = webdriver.Firefox(options=options)
      # 安装扩展程序 (addons)  可选，替换为扩展程序路径
      # browser.install_addon("D:/Application/Browser/webdriver/selenium_ide-3.17.4.xpi")

      # 企業情報
      # https://www.reuters.com/markets/companies/5401.T
      url = 'https://www.reuters.com/markets/companies/{symbol}.T'

      for row in EquityProfile.select(EquityProfile.symbol).where(EquityProfile.symbol.in_(symbol)):
        print(url.format(symbol=row.symbol))
        driver.get(url.format(symbol=row.symbol))
        # assert 'Yahoo' in browser.title
        # 等待搜索结果加载
        # browser.implicitly_wait(10)

        # statistics = browser.find_element(By.XPATH,  "//dl[@class='company-profile-maximizer__statistics__-mFht']")
        # items = browser.find_element(By.XPATH, "//dl[@class='company-profile-maximizer__stats-row__3jpfi']")

        statistics = driver.find_elements(By.XPATH, "//dl[@class='company-profile-maximizer__statistics__-mFht'] | //dl[@class='company-profile-maximizer__stats-row__3jpfi']")
        for statistic in statistics:
          matches = re.split(r"\n", statistic.text)
          for i in range(0, len(matches), 2):
            key, value =  matches[i], matches[i + 1]
            if key in mapping.keys():
              key = mapping[key]
              setattr(row, key, value)

        database.update(row, fields=['debt_equity_ratio'])
    except:
      traceback.print_exc()
    finally:
      # 关闭浏览器
      driver.quit()


    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")



if __name__ == '__main__':
  Reuters.update_equity_statistics('1301', '2130')

