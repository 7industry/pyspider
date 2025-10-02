#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 目標株価まとめ  値上がり率 / 値下がり率ランキング  Price Increase / Price Decrease Ranking
# https://www.kabuka.jp.net/neagari-nesagari.html

import re
import time
import random
import traceback

from mechanicalsoup import StatefulBrowser

from config.env import useragents, timeout

class Jpx:

    # 退市股票
    @staticmethod
    def get_delisted():
        try:
            profiles = []
            urls = [
                "https://www.jpx.co.jp/listing/stocks/delisted/index.html",
                "https://www.jpx.co.jp/listing/stocks/delisted/archives-01.html"
            ]

            for url in urls:
                browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
                browser.open(url, timeout=timeout)
                browser.close()

                rows = browser.page.select("div#readArea div.component-normal-table table tbody tr")

                for row in rows:
                    cells = row.find_all("td")
                    if len(cells) >= 5:
                        delist_date = cells[0].get_text(strip=True)
                        name = cells[1].get_text(strip=True)
                        symbol = cells[2].get_text(strip=True)
                        exchange = cells[3].get_text(strip=True)
                        reason = cells[4].get_text(strip=True)

                        # print(f"上場廃止日：{delist_date} 銘柄名：{name} コード：{symbol} 市場区分：{exchange} 上場廃止理由：{reason}")
                        profiles.append((symbol, delist_date))

        except:
            traceback.print_exc()
        else:
            return profiles
        finally:
            pass



    # 获取节假日
    @staticmethod
    def get_holiday_list():
        # 使用 time() 函数
        start_time = time.time()

        url = "https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html"
        browser = StatefulBrowser(user_agent=useragents[random.randint(0, len(useragents) - 1)])
        browser.open(url, timeout=timeout)
        browser.close()

        holidays = []

        if browser.page:
            cells = browser.page.select("div.component-normal-table table.overtable tr td")

            for i in range(0, len(cells), 2):
                day = cells[i].get_text(strip=True)
                name = cells[i + 1].get_text(strip=True)

                # Remove Japanese weekday in parentheses
                day = re.sub(r"（[月火水木金土日]）", "", day)

                print(f"日付：{day} 名称：{name}")
                holidays.append(day)

        # 计算耗时
        end_time = time.time()
        elapsed_time = end_time - start_time

        print("耗时:", elapsed_time, "秒")

        return holidays
