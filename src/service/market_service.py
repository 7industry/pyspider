#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test
# Date:      2020/4/14
__Author__ = 'chen'
#-------------------------------------------------------------------------------
import asyncio
import time
import traceback
from datetime import datetime, date
from typing import List, Tuple

from api import database
from config.env import items_per_run

from headless.kabumap import Kabumap
from headless.kabuyoho import Kabuyoho
from headless.minkabu import Minkabu
from headless.nikkei import Nikkei
from headless.kabuka import Kabuka
from headless.yahoo import Yahoo
from model.SchemaModel import EquityProfile

class MarketService:

  # 静态类变量（所有实例共享）
  black_list = set()

  # 上場廃止銘柄一覧（所有实例共享）
  delisted_list : List[Tuple[str, str]] = []

  #  交易日
  trading_date = None

  # 单个删除
  @classmethod
  def delete_stock(cls, symbol):
      database.delete(EquityProfile, symbol)
      # 根据主键删除 Person 实例
      # EquityProfile.delete().where(EquityProfile.symbol == symbol).execute()


  # 开始下载
  @classmethod
  async def download(cls, *symbols):
    # 遍历查询结果
    for symbol in symbols:
      try:
        # Format the current date to YYYYMMDD
        current_date = date.today().strftime("%Y%m%d")

        # check data
        profile = EquityProfile.select().where(EquityProfile.symbol == symbol).first()
        # profile = database.get(EquityProfile, symbol) # TODO  ERROR
        if profile and profile.update_date and profile.update_date >= current_date:
          return

        await asyncio.sleep(2)

        base_data = Nikkei(symbol=symbol).update()
        base_data = Minkabu(base_data).update()
        base_data = Kabumap(base_data).update()
        base_data = Kabuyoho(base_data).update()
        base_data = Yahoo(base_data).update()

        # 日期
        setattr(base_data.record, 'update_date', cls.trading_date)

        # 新規 OR 更新
        if profile:
          base_data.save()
        else:
          base_data.insert()

        # await asyncio.gather()
      except:
        # 上場廃止日 更新
        for delisted_symbol, delisted_date in cls.delisted_list:
          if symbol == delisted_symbol:
            found = True

            # 转换为 datetime 对象
            date1 = datetime.strptime(cls.trading_date, "%Y/%m/%d")
            date2 = datetime.strptime(delisted_date, "%Y/%m/%d")

            # 比较大小
            if date1 >= date2:
              equity_profile = EquityProfile()
              equity_profile.symbol = symbol
              equity_profile.delisting_date = delisted_date
              print(f"上場廃止更新   コード：{delisted_symbol} 上場廃止日：{delisted_date}")
              equity_profile.save()
            break

        if not found:
          cls.black_list.add(symbol)

        traceback.print_exc()
        # Signal the main program to terminate
        asyncio.get_event_loop().stop()
        # raise
      finally:
        pass


  # ランニングによって更新
  @classmethod
  def ranking_down(cls):
    Kabuka.update_ranking_profile()


  # 随机下载
  @classmethod
  def random_down(cls):
      # 使用 time() 函数
      start_time = time.time()

      # database.find(row, fields=['credit_multiplier'])
      # profiles = EquityProfile.select().where(EquityProfile.update_date == None).order_by(EquityProfile.update_date.asc())

      # 查询随机 200 条记录
      # profiles = EquityProfile.select(EquityProfile.symbol, EquityProfile.name).order_by(EquityProfile.update_date.asc(), EquityProfile.symbol.desc()).limit(200)
      # profiles = EquityProfile.select().order_by(EquityProfile.update_date.asc(), peewee.fn.random()).limit(200)
      profiles = database.get_random(EquityProfile, 200)

      # 遍历查询结果
      for profile in profiles:
          # 打印结果
          now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(f"[{now}] 代码：{profile.symbol} 名称：{profile.name}")

          asyncio.run(cls.download(profile.symbol))


      # 计算耗时
      end_time = time.time()
      elapsed_time = end_time - start_time

      print("耗时:", elapsed_time, "秒")


  # 批量下载
  @classmethod
  def batch_down(cls):
      # 使用 time() 函数
      start_time = time.time()

      # database.find(row, fields=['credit_multiplier'])
      # profiles = EquityProfile.select().where(EquityProfile.update_date == None).order_by(EquityProfile.update_date.asc())

      # 查询前 200 条记录
      # profiles = [item for item in EquityProfile.select(EquityProfile.symbol, EquityProfile.name).order_by(EquityProfile.update_date.asc()).limit(200)]

      # profiles = cls.get_batch_symbol("2025-10-01", 20)

      profiles = cls.get_batch_symbol()

      # 遍历查询结果
      if not profiles:
        print("查询结果为空")
        cls.black_list = set()
      else:
        for profile in profiles:
          # 打印结果
          now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          print(f"[{now}] 代码：{profile.symbol} 名称：{profile.name}")

          asyncio.run(cls.download(profile.symbol))


      # 计算耗时
      end_time = time.time()
      elapsed_time = end_time - start_time

      print("耗时:", elapsed_time, "秒")



  @classmethod
  def get_batch_symbol(cls):
    profiles = (EquityProfile
             .select(EquityProfile.symbol, EquityProfile.name, EquityProfile.update_date)
             .where(
      (EquityProfile.update_date != cls.trading_date) | (EquityProfile.update_date.is_null(True)),
      EquityProfile.delisting_date.is_null(True),
      EquityProfile.symbol.not_in(cls.black_list)
    )
             .order_by(EquityProfile.update_date.asc())
             .limit(items_per_run))

    # profiles = [(item.symbol, item.name, item.update_date) for item in query]
    return list(profiles)





if __name__ == '__main__':
    # MarketService.delete_stock(3504)
    # asyncio.run(MarketService.download(4875))
    MarketService.batch_down()
