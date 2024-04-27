#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 目標株価まとめ  値上がり率 / 値下がり率ランキング  Price Increase / Price Decrease Ranking
# https://www.kabuka.jp.net/neagari-nesagari.html
import asyncio
import random
import re
from mechanicalsoup import StatefulBrowser

from src.config.env import useragents


class Kabuka:

  @classmethod
  def update_ranking_profile(cls):

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

        from src.service.market_service import MarketService
        asyncio.run(MarketService.download(symbol))

