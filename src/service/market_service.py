#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:      test
# Date:      2020/4/14
__Author__ = 'chen'
#-------------------------------------------------------------------------------
import asyncio
import sys
import traceback

from src.api import database
import time

from src.headless.kabumap import Kabumap
from src.headless.kabuyoho import Kabuyoho
from src.headless.minkabu import Minkabu
from src.headless.nikkei import Nikkei
from src.headless.yahoo import Yahoo
from src.model.FundamentalData import CompanyProfile

class MarketService:

  # 单个删除
  @classmethod
  def delete_stock(cls, symbol):
      database.delete(CompanyProfile, symbol)
      # 根据主键删除 Person 实例
      # CompanyProfile.delete().where(CompanyProfile.symbol == symbol).execute()


  # 随机下载
  @classmethod
  def random_down(cls):
      # 使用 time() 函数
      start_time = time.time()

      # database.find(row, fields=['credit_multiplier'])
      # profiles = CompanyProfile.select().where(CompanyProfile.update_date == None).order_by(CompanyProfile.update_date.asc())

      # 查询前 200 条记录
      profiles = CompanyProfile.select(CompanyProfile.symbol,CompanyProfile.name).order_by(CompanyProfile.update_date.asc(), CompanyProfile.symbol.desc()).limit(200)

      # 遍历查询结果
      for profile in profiles:
          # 打印结果
          print(f"代码：{profile.symbol} 名称：{profile.name}")
          # 运行事件循环
          asyncio.run(cls.update_profile(profile.symbol))

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
        raise
      finally:
        pass

  # 开始下载
  @classmethod
  def download(self, symbol):
    print(f"symbol：{symbol} start...")

    Kabumap.update_company_profile(symbol)
    Nikkei.update_company_profile(symbol)
    Kabuyoho.update_company_profile(symbol)
    Minkabu.update_company_profile(symbol)
    Yahoo.update_company_profile(symbol)
    print(f"symbol：{symbol} end!")


if __name__ == '__main__':
    # MarketService.delete_stock(3504)
    # MarketService.download(4875)
    MarketService.random_down()
