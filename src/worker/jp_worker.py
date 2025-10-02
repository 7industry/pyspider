#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import pytz
from datetime import datetime, timedelta, date

from config.env import delay_between_runs
from headless.jpx import Jpx
from service.market_service import MarketService

# from headless.kabumap import Kabumap
# from headless.kabuyoho import Kabuyoho
# from headless.minkabu import Minkabu
# from headless.nikkei import Nikkei
# from headless.reuters import Reuters
# from headless.toyokeizai import Toyokeizai
# from headless.yahoo import Yahoo
# from model.SchemaModel import EquityProfile


# Kabumap.update_equity_statistics('6659')
# Nikkei.update_equity_statistics('6659')
# Kabuyoho.update_equity_statistics('6659')
# Minkabu.update_equity_statistics('6659')
# Yahoo.update_equity_statistics('6659')

# Reuters.update_equity_statistics('6659')

# Toyokeizai.update_equity_statistics('6659')


# 设置东京时区
tokyo_tz = pytz.timezone('Asia/Tokyo')

# 非交易日判断
def is_holiday():
  return datetime.now().strftime("%Y/%m/%d") in holidays

# 判断是否是下午4点（16点）或早上8点之前
def is_target_time():
  # 获取当前东京时间
  now_tokyo = datetime.now(tokyo_tz)
  hour = now_tokyo.hour
  return hour >= 16 or hour < 8


# 获取最后的交易日
def get_last_business_date():
  current_time =  datetime.now()
  last_bus_date = current_time.date()

  # 如果当前时间在 16:00 之前，回退一天
  if current_time.hour < 16:
    last_bus_date -= timedelta(days=1)

  # 回退到最近的非节假日工作日
  while (last_bus_date.weekday() >= 5 or  # 5=Saturday, 6=Sunday
         last_bus_date.strftime("%Y/%m/%d") in holidays):
    last_bus_date -= timedelta(days=1)

  return last_bus_date.strftime("%Y/%m/%d")

# 获取节假日
holidays = Jpx.get_holiday_list()

# 退市股票
MarketService.delisted_list = Jpx.get_delisted()

while True:
  if is_holiday() or is_target_time():
    MarketService.trading_date = get_last_business_date()
    print(f"当前下载交易数据日期是： {MarketService.trading_date} ")
    MarketService.batch_down()

  # 每10分钟检查一次（600秒）
  time.sleep(delay_between_runs)
