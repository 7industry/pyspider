#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from mechanicalsoup import StatefulBrowser
from src.config.env import useragents
from src.headless.dataintegrator import DataIntegrator
from src.model.FundamentalData import CompanyProfile
from src.api import database


class Minkabu(DataIntegrator):

  _fields = ['listing_date', 'tel']

  __mapping = {
    '上場市場': 'exchange',
    '上場年月日': 'listing_date',
    '単元株数': 'per_unit',
    '住所': 'address',
    '電話番号(IR)': 'tel',
    '資本金': 'capital_stock',
  }

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      '上場市場': 'exchange',
      '上場年月日': 'listing_date',
      '単元株数': 'per_unit',
      '住所': 'address',
      '電話番号(IR)': 'tel',
      '資本金': 'capital_stock',
    }

    # 企業情報
    # https://minkabu.jp/stock/7003/fundamental
    url = 'https://minkabu.jp/stock/{symbol}/fundamental'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      # 株式（上場市場）の状況
      stock_listed_market_status = [element.text for element in browser.page.select('div[class="ly_content_wrapper"] dl[class="md_dataList"]')]

      # 遍历所有元素并获取文本内容
      for element in stock_listed_market_status:
        matches = re.findall(r"(\S+.*?)\n+", element)
        for i in range(0, len(matches), 2):
          key, value = matches[i], matches[i + 1]
          if key in mapping.keys():
            key = mapping[key]
            setattr(row, key, value)

      database.update(row, fields=['listing_date', 'tel'])

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")


  def get_company_profile(self):
    # 使用 time() 函数
    start_time = time.time()

    row = CompanyProfile()
    row.symbol = self.symbol

    # 企業情報
    # https://minkabu.jp/stock/7003/fundamental
    url = 'https://minkabu.jp/stock/{symbol}/fundamental'

    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
    # 使用 format() 方法替换字符串
    print(url.format(symbol=row.symbol))
    browser.open(url.format(symbol=row.symbol))
    browser.close()

    # 株式（上場市場）の状況
    stock_listed_market_status = [element.text for element in browser.page.select('div[class="ly_content_wrapper"] dl[class="md_dataList"]')]

    # 遍历所有元素并获取文本内容
    for element in stock_listed_market_status:
      matches = re.findall(r"(\S+.*?)\n+", element)
      for i in range(0, len(matches), 2):
        key, value = matches[i], matches[i + 1]
        if key in self.__mapping.keys():
          key = self.__mapping[key]
          setattr(row, key, value)


    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

    # database.update(row, fields=['listing_date', 'tel'])
    return row
