#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import time
import random
from mechanicalsoup import StatefulBrowser
from src.config.env import useragents
from src.model.FundamentalData import CompanyProfile
from src.api import database


class Kabuyoho:

  @classmethod
  def update_company_profile(cls, *symbol):
    # 使用 time() 函数
    start_time = time.time()
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

    mapping = {
      '時価総額': 'market_cap',
      'レーティング': 'grade_rating',
      'PER(予)': 'per',
      'PBR(実)': 'pbr',
      'ROA(実)': 'roa',
      'ROE(実)': 'roe',
      '配当利回り(予)': 'dividend_yield',
      '自己資本比率': 'own_capital_ratio',
      '事業内容': 'business_scope',
      '取扱い商品': 'product_range',
    }

    # 企業情報
    # https://kabuyoho.jp/reportTop?bcode=5020
    url = 'https://kabuyoho.jp/reportTop?bcode={symbol}'

    for row in CompanyProfile.select(CompanyProfile.symbol).where(CompanyProfile.symbol.in_(symbol)):
      # 使用 format() 方法替换字符串
      print(url.format(symbol=row.symbol))
      browser.open(url.format(symbol=row.symbol))

      # 株式状況
      elements = [element.text for element in browser.page.select('div[class="smary_box"] dl > :is(dt,dd)')]

      for i in range(0, len(elements), 2):
        keys, values = elements[i], elements[i + 1]
        keys = re.findall(r"(\S+.*?)\n+", keys)
        values = re.findall(r"(\S+.*?)\n+", values)

        key, value = keys[0], values[0]
        if key in mapping.keys():
          key = mapping[key]
          setattr(row, key, value)

      # elements = [element.text for element in browser.page.select('section[class="info_box info_box_contents"]')]
      elements = browser.page.select('section[class="info_box info_box_contents"], section[class="info_box info_box_product"]')

      if len(elements) > 0:
        # 事業内容
        business_titel = elements[0].select('h2')[0].text.strip()
        business_scope = "\n".join(p.text.strip() for p in elements[0].select("section > p"))
        setattr(row,  mapping[business_titel], business_scope)

        # 取扱い商品
        product_titel = elements[1].select('h2')[0].text.strip()
        product_range = "\n".join(p.text.strip() for p in elements[1].select("section > p"))
        setattr(row, mapping[product_titel], product_range)

        database.update(row, fields=['market_cap', 'grade_rating', 'own_capital_ratio', 'business_scope', 'product_range', 'dividend_yield'])
      else:
        print('ウェブサイト「株予報プロ」に、銘柄「{symbol}」は登録されていません'.format(symbol=row.symbol))


    browser.close()

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")

