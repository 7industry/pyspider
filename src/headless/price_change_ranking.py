#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 目標株価まとめ  値上がり率 / 値下がり率ランキング  Price Increase / Price Decrease Ranking
# https://www.kabuka.jp.net/neagari-nesagari.html


import time
import random
import re
import traceback
from mechanicalsoup import StatefulBrowser

from src.config.env import useragents

import asyncio

from src.headless.kabumap import Kabumap
from src.headless.kabuyoho import Kabuyoho
from src.headless.minkabu import Minkabu
from src.headless.nikkei import Nikkei
from src.headless.yahoo import Yahoo

class Kabuka:

  @classmethod
  def update_company_profile(cls):

    # 使用 time() 函数
    start_time = time.time()

    url = 'https://www.kabuka.jp.net/neagari-nesagari.html'
    browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
    browser.open(url)
    browser.close()

    # 查找 ID 为 readmoretable 的 div
    elements = browser.page.select('div.readmoretable > div.readmoretable_line')

    # 遍历所有元素并打印它们的文本
    for element in elements:
      # 使用正则表达式匹配数据
      matches = re.findall(r"(\S+.*?)\s+\((\d*?)\)\s+(.*?)\s+(.*?)\s+(\S+.*?)\s*", element.text)

      # 提取所需数据
      for match in matches:
        name = match[0]
        symbol = match[1]
        exchange = match[2]
        change = match[3]
        percentage = match[4]

        # 打印结果
        print(f"交易所：{exchange} 代码：{symbol} 名称：{name} 涨幅：{change} 百分比：{percentage}")
        # 运行事件循环
        asyncio.run(cls.update_profile(symbol))

    # 计算耗时
    end_time = time.time()
    elapsed_time = end_time - start_time

    print("耗时:", elapsed_time, "秒")


  async def update_profile(symbol):
    try:
      await asyncio.sleep(2)
      Kabumap.update_company_profile(symbol)
      Nikkei.update_company_profile(symbol)
      Kabuyoho.update_company_profile(symbol)
      Minkabu.update_company_profile(symbol)
      Yahoo.update_company_profile(symbol)
      # await asyncio.gather()
    except:
      traceback.print_exc()
    finally:
      pass

if __name__ == '__main__':
    Kabuka.update_company_profile()