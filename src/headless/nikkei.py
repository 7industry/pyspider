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


class Nikkei(DataIntegrator):

  _fields = ['established_date', 'sector', 'industry', 'index_adoption', 'url', 'representative', 'per_unit', 'address', 'capital_stock']

  __mapping = {
    '設立年月日': 'established_date',
    '日経業種分類': 'industry',
    '東証業種名': 'sector',
    '指数採用': 'index_adoption',
    'URL': 'url',
    '代表者氏名': 'representative',
    '売買単位': 'per_unit',
    '本社住所': 'address',
    '電話番号': 'tel',
    '資本金': 'capital_stock',
  }

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      '設立年月日': 'established_date',
      '日経業種分類': 'industry',
      '東証業種名': 'sector',
      '指数採用': 'index_adoption',
      'URL': 'url',
      '代表者氏名': 'representative',
      '売買単位': 'per_unit',
      '本社住所': 'address',
      '電話番号': 'tel',
      '資本金': 'capital_stock',
    }

    # 企業情報
    # https://www.nikkei.com/nkd/company/gaiyo/?scode=7003
    url = 'https://www.nikkei.com/nkd/company/gaiyo/?scode={symbol}'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      for tr in browser.page.select('div[class="m-articleFrame_body"] table tr')[:22]:
        matches = re.findall(r"(\S+.*?)\n+", tr.text)
        key = matches[0]
        value = matches[1]

        if key in mapping.keys():
          key = mapping[key]
          setattr(row, key, value)

      database.update(row, fields=['established_date', 'sector', 'industry', 'index_adoption', 'url', 'representative', 'per_unit', 'address', 'capital_stock'])

    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")


  def get_company_profile(self):
    # 使用 time() 函数
    start_time = time.time()

    # for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):

    row = CompanyProfile()
    row.symbol = self.symbol

    # 企業情報
    # https://www.nikkei.com/nkd/company/gaiyo/?scode=7003
    url = 'https://www.nikkei.com/nkd/company/gaiyo/?scode={symbol}'

    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
    # 使用 format() 方法替换字符串
    print(url.format(symbol=row.symbol))
    browser.open(url.format(symbol=row.symbol))
    browser.close()


    for tr in browser.page.select('div[class="m-articleFrame_body"] table tr')[:22]:
      matches = re.findall(r"(\S+.*?)\n+", tr.text)
      key = matches[0]
      value = matches[1]

      if key in self.__mapping.keys():
        key = self.__mapping[key]
        setattr(row, key, value)


    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

    # database.update(row, fields=['established_date', 'sector', 'industry', 'index_adoption', 'url', 'representative', 'per_unit', 'address', 'capital_stock'])
    return row

