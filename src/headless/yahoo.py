#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://finance.yahoo.com/quote/7003.T
import re
import time
import random
from datetime import datetime
from mechanicalsoup import StatefulBrowser

from api import database
from config.env import useragents, timeout
from headless.dataintegrator import DataIntegrator
from model.SchemaModel import EquityProfile


class Yahoo(DataIntegrator):

  _fields =['market_cap', 'enterprise_value', 'ex_dividend_date', 'year_low', 'year_high',
             'year_change_ratio', 'pbr', 'per', 'roa', 'roe', 'eps', 'dividend_yield',
             'book_value_per_share', 'debt_equity_ratio', 'update_date']

  mapping = {
    'Market Cap': 'market_cap',
    'Enterprise Value': 'enterprise_value',
    'Beta': 'beta',
    'Price/Book': 'pbr',
    'Trailing P/E': 'per',
    'Return on Assets': 'roa',
    'Return on Equity': 'roe',
    'Diluted EPS': 'eps',
    '52 Week Low': 'year_low',
    '52 Week High': 'year_high',
    '52 Week Range': 'year_change_ratio',
    'Forward Annual Dividend Yield': 'dividend_yield',
    'Ex-Dividend Date': 'ex_dividend_date',
    'Book Value Per Share': 'book_value_per_share',
    'Total Debt/Equity': 'debt_equity_ratio',
  }

  @classmethod
  def update_equity_statistics(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      'Market Cap': 'market_cap',
      'Enterprise Value': 'enterprise_value',
      'Beta': 'beta',
      'Price/Book': 'pbr',
      'Trailing P/E': 'per',
      'Return on Assets': 'roa',
      'Return on Equity': 'roe',
      'Diluted EPS': 'eps',
      '52 Week Low': 'year_low',
      '52 Week High': 'year_high',
      '52 Week Range': 'year_change_ratio',
      'Forward Annual Dividend Yield': 'dividend_yield',
      'Ex-Dividend Date': 'ex_dividend_date',
      'Book Value Per Share': 'book_value_per_share',
      'Total Debt/Equity': 'debt_equity_ratio',
    }

    # 企業情報
    # https://finance.yahoo.com/quote/5020.T/key-statistics
    url = 'https://finance.yahoo.com/quote/{symbol}.T/key-statistics'

    for row in EquityProfile.select(EquityProfile.symbol).where(EquityProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol), timeout=timeout)

      for element in browser.page.select('div:is(.table-container, .container) table tr'):
        elements = element.select('td:not(sup)')
        # elements = element.select('td:not(sup)')
        # td_text = element.select('td:not(sup)').get_text()
        if(elements):
          key, value = elements[0].contents[0].strip(), elements[1].text.strip()
          # 剔除掉 () 之间的内容
          key = re.sub(r"\(.*?\)", "", key)

          if (value != '--'):
            if (key == 'Ex-Dividend Date'):
              # 将日期字符串转换为 datetime 对象
              date = datetime.strptime(value, "%m/%d/%Y")
              # 将 datetime 对象转换为 yyyymmdd 格式
              value = date.strftime("%Y%m%d")

            if key in mapping.keys():
              key = mapping[key]
              setattr(row, key, value)

      database.update(row, fields=cls._fields)

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")


  def get_equity_statistics(self):
    # 使用 time() 函数
    start_time = time.time()
    row = EquityProfile()
    row.symbol = self.symbol

    # for row in EquityProfile.select(EquityProfile.symbol).where(EquityProfile.symbol.in_(symbol)):

    # 企業情報
    # https://finance.yahoo.com/quote/5020.T/key-statistics
    url = 'https://finance.yahoo.com/quote/{symbol}.T/key-statistics'

    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
    # 使用 format() 方法替换字符串
    print(url.format(symbol=row.symbol))
    browser.open(url.format(symbol=row.symbol), timeout=timeout)
    browser.close()

    if browser.page:
      for element in browser.page.select('div:is(.table-container, .container) table tr'):
        elements = element.select('td')
        # elements = element.select('td:not(sup)')
        # td_text = element.select('td:not(sup)').get_text()
        if elements:
          key, value = elements[0].contents[0].strip(), elements[1].text.strip()
          # 剔除掉 () 之间的内容
          key = re.sub(r"\(.*?\)", "", key).strip()

          if (value != '--'):
            if (key == 'Ex-Dividend Date'):
              # 将日期字符串转换为 datetime 对象
              date = datetime.strptime(value, "%m/%d/%Y")
              # 将 datetime 对象转换为 yyyymmdd 格式
              value = date.strftime("%Y%m%d")

            if key in self.mapping.keys():
              key = self.mapping[key]
              setattr(row, key, value)

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

    return row
