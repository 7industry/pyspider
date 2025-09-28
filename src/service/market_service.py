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
import datetime

from api import database

from headless.kabumap import Kabumap
from headless.kabuyoho import Kabuyoho
from headless.minkabu import Minkabu
from headless.nikkei import Nikkei
from headless.kabuka import Kabuka
from headless.yahoo import Yahoo
from model.SchemaModel import EquityProfile

class MarketService:

  # 单个删除
  @classmethod
  def delete_stock(cls, symbol):
      database.delete(EquityProfile, symbol)
      # 根据主键删除 Person 实例
      # EquityProfile.delete().where(EquityProfile.symbol == symbol).execute()


  # 开始下载
  @classmethod
  async def download(cls, *symbols):
      try:
        # 遍历查询结果
        for symbol in symbols:
          # Format the current date to YYYYMMDD
          current_date = datetime.date.today().strftime("%Y%m%d")

          # check data
          profile = EquityProfile.select().where(EquityProfile.symbol == symbol).first()
          # profile = database.get(EquityProfile, symbol) # TODO  ERROR
          if profile and profile.update_date and profile.update_date >= current_date:
              return

          await asyncio.sleep(2)

          baseData = Kabumap(symbol=symbol).update()
          baseData = Nikkei(baseData).update()
          baseData = Kabuyoho(baseData).update()
          baseData = Minkabu(baseData).update()
          baseData = Yahoo(baseData).update()

          # 新規 OR 更新
          if profile:
            baseData.save()
          else:
            baseData.insert()

          # await asyncio.gather()
      except:
        traceback.print_exc()
        # Signal the main program to terminate
        asyncio.get_event_loop().stop()
        raise
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
          print(f"代码：{profile.symbol} 名称：{profile.name}")

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
      profiles = [item for item in EquityProfile.select(EquityProfile.symbol, EquityProfile.name).order_by(EquityProfile.update_date.asc()).limit(200)]

      # 遍历查询结果
      for profile in profiles:
          # 打印结果
          print(f"代码：{profile.symbol} 名称：{profile.name}")

          asyncio.run(cls.download(profile.symbol))


      # 计算耗时
      end_time = time.time()
      elapsed_time = end_time - start_time

      print("耗时:", elapsed_time, "秒")






if __name__ == '__main__':
    # MarketService.delete_stock(3504)
    # asyncio.run(MarketService.download(4875))
    MarketService.batch_down()
