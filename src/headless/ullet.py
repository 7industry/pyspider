#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 上場企業約4000社をワンクリックで分析   Analyze approximately 4,000 listed companies with one click

# 注目度
#     過去３年分の決算書が存在する企業について、企業の財務状態や市場の評価等をもとに注目度を表示します。
# ※注目度は当サイトの独自のルールに基づいて算出したものであり、正確性・完全性についていかなる保証をするものでもありません。情報収集や状況判断については利用者ご自身の責任において行って下さい。
#
# 企業名
# 	 企業名をクリックすると、その企業の早わかりページを見ることができます。また、企業名にマウスカーソルを当てると、企業の概要や、業績などの指標が分かる「企業メニュー」が表示されます。

# https://www.ullet.com/search.html
# https://www.ullet.com/search/page/1.html?without_layout
# https://www.ullet.com/search/disp/1/page/196.html?without_layout

import time
import random
import re
from mechanicalsoup import StatefulBrowser

from api import database
from config.env import useragents, timeout

# Set Cookie Jar so we can stay logged in...
# br.set_cookiejar(cookie_jar)
from model.SchemaModel import EquityProfile
from util.cvs_handler import CsvHandler


def save_data(brief_elements, disp_elements):
  """Return the key associated to a registered file object.

  Returns:
  SelectorKey for this file object
  """

  data = []
  # 遍历 list 并添加新属性
  entities = []

  # 使用 for 循环
  for i in range(len(brief_elements)):
    # 使用正则表达式匹配数据
    brief_matches = re.findall(r"(\S+.*?)\n+", brief_elements[i].text)
    disp_matches = re.findall(r"(\S+.*?)\n+", disp_elements[i].text)

    # 提取所需数据
    spotlight = brief_elements[i].contents[3].contents[0].attrs['title'].strip()  # 注目度
    name = brief_matches[1].strip()  # 企業名
    symbol = brief_matches[2].strip()  # コード
    sector = brief_matches[3].strip()  # 業種
    exchange = brief_matches[4].strip()  # 市場名
    amount_of_sales = brief_matches[5].strip()  # 売上高

    # 打印结果
    # print(f"順位：{number}")
    # print(f"企業名：{name}")
    # print(f"コード：{symbol}")
    # print(f"業種：{sector}")
    # print(f"市場名：{exchange}")
    # print(f"売上高：{amountOfSales}")

    # number = disp_matches[0]  # 順位
    # name = disp_matches[1]  # 企業名
    # amount_of_sales = disp_matches[2]  # 売上高
    net_income = disp_matches[3].strip()  # 当期純利益
    sales_cf= disp_matches[4].strip()  # 営業C/F
    total_assets = disp_matches[5].strip()  # 総資産
    cash_and_deposits = disp_matches[6].strip()  # 現預金等
    total_capital = disp_matches[7].strip()  # 資本合計
    average_annual_income = disp_matches[8].strip()  # 平均年収

    # 打印结果
    # print(f"順位：{number}")
    # print(f"企業名：{name}")
    # print(f"売上高：{amount_of_sales}")
    # print(f"当期純利益：{net_income}")
    # print(f"営業C/F：{sales_cf}")
    # print(f"総資産：{total_assets}")
    # print(f"現預金等：{cash_and_deposits}")
    # print(f"資本合計：{total_capital}")
    # print(f"平均年収：{average_annual_income}")
    assert (brief_matches[1] == disp_matches[1]) & (brief_matches[5] == disp_matches[2]), "順位 {} 必须是同一家企业: {} {} {} {}".format(brief_matches[1], brief_matches[1], disp_matches[1], brief_matches[5], disp_matches[2])

    # 创建一个列表
    # data.append([symbol, number, name, sector, exchange, amount_of_sales, net_income, sales_cf, total_assets, cash_and_deposits, total_capital, average_annual_income])
    entity = EquityProfile(symbol=symbol, spotlight=spotlight, name=name, sector=sector
                            , exchange=exchange, amount_of_sales=amount_of_sales, net_income=net_income
                            , sales_cf=sales_cf, total_assets=total_assets, cash_and_deposits=cash_and_deposits
                            , total_capital=total_capital, average_annual_income=average_annual_income)
    entities.append(entity)

  header = ["コード", "注目度", "企業名", "業種", "市場名", "売上高", "当期純利益", "営業C/F", "総資産", "現預金等", "資本合計", "平均年収"]

  # CsvHandler.export_csv(header=header,data=data)

  # データ登録
  database.insert_many(*entities)


# 使用 time() 函数
start_time = time.time()

total_pages = 197
for i in range(total_pages):
  i = i + 1

  browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])

  brief_url = 'https://www.ullet.com/search/page/{}.html?without_layout'
  disp_url = 'https://www.ullet.com/search/disp/1/page/{}.html?without_layout'

  print(brief_url.format(i))
  browser.open(brief_url.format(i), timeout=timeout)
  # 查找 ID 为 list 开头的  <tr id="list7203" class="even first">
  brief_elements = browser.page.select('table > tr[id^="list"]')

  print(disp_url.format(i))
  browser.open(disp_url.format(i), timeout=timeout)
  disp_elements = browser.page.select('table > tr[id^="list"]')

  save_data(brief_elements,disp_elements)



end_time = time.time()

# 计算耗时
elapsed_time = end_time - start_time

print("耗时:", elapsed_time, "秒")
