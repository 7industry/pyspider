#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# https://finance.yahoo.com/quote/7003.T
import time
import random
from datetime import datetime
from mechanicalsoup import StatefulBrowser

from src.api import database
from src.config.env import useragents
from src.model.FundamentalData import CompanyProfile


class Yahoo:

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      'Enterprise Value': 'enterprise_value',
      'Beta': 'beta',
      'Price/Book': 'pbr',
      'Trailing P/E': 'per',
      'Return on Assets': 'roa',
      'Return on Equity': 'roe',
      'Diluted EPS': 'eps',
      '52 Week Low': 'year_low',
      '52 Week High': 'year_high',
      '52-Week Change': 'year_change_ratio',
      'Forward Annual Dividend Yield': 'dividend_yield',
      'Ex-Dividend Date': 'ex_dividend_date',
      'Book Value Per Share': 'book_value_per_share',
      'Total Debt/Equity': 'debt_equity_ratio',
    }

    # 企業情報
    # https://finance.yahoo.com/quote/5020.T/key-statistics
    url = 'https://finance.yahoo.com/quote/{symbol}.T/key-statistics'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      elements = [element for element in browser.page.select('div[id="Main"] table tr td')]

      for i in range(0, len(elements), 2):
        key, value = elements[i].select('span')[0].text.strip(), elements[i + 1].text.strip()

        if (key == 'Ex-Dividend Date' and value != 'N/A'):
          # 将日期字符串转换为 datetime 对象
          date = datetime.strptime(value, "%b %d, %Y")
          # 将 datetime 对象转换为 yyyymmdd 格式
          value = date.strftime("%Y%m%d")

        if key in mapping.keys():
          key = mapping[key]
          setattr(row, key, value)

      database.update(row, fields=['enterprise_value', 'ex_dividend_date', 'year_low', 'year_high', 'year_change_ratio', 'pbr', 'per', 'roa', 'roe', 'eps', 'dividend_yield', 'book_value_per_share', 'debt_equity_ratio', 'update_date'])

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

