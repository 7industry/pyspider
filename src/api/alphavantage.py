#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import traceback
import csv


from api import database
from model.SchemaModel import CompanyOverview, IncomeStatement, BalanceSheet, CashFlow, Earnings, ListingStatus

# https://www.alphavantage.co/support/#api-key
apikey = "RSNV5C041ETQCGWI"


def company_overview(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=OVERVIEW&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        #　属性名の変換
        entity = CompanyOverview.from_json(data)

        # データ登録
        # database.save(entity)

        # データ登録
        entity = entity.to_json()
        database.insert(CompanyOverview, **entity)
    except:
        print("company_overview except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass

def income_statement(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={apikey}'

        url = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(IncomeStatement.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(IncomeStatement.from_json(report))

        # データ登録
        database.insert_many(*entities)
    except:
        print("income_statement except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass



def balance_sheet(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(BalanceSheet.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(BalanceSheet.from_json(report))

        # データ登録
        database.insert_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def cash_flow(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=CASH_FLOW&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualReports']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(CashFlow.from_json(report))

        for report in data['quarterlyReports']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(CashFlow.from_json(report))

        # データ登録
        database.insert_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def earnings(symbol):
    try:
        url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={apikey}'
        url = "https://www.alphavantage.co/query?function=EARNINGS&symbol=IBM&apikey=demo"

        # 使用 format() 方法替换字符串
        url = url.format(symbol=symbol, apikey=apikey)
        print(url)

        r = requests.get(url)
        data = r.json()

        # 遍历 list 并添加新属性
        entities = []
        for report in data['annualEarnings']:
            report["ReportType"] = "annualReports"
            report["Symbol"] = data["symbol"]
            entities.append(Earnings.from_json(report))

        for report in data['quarterlyEarnings']:
            report["ReportType"] = "quarterlyReports"
            report["Symbol"] = data["symbol"]
            entities.append(Earnings.from_json(report))

        # データ登録
        database.insert_many(*entities)
    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        return data
    finally:
        pass


def listing_status():
    try:
        # Querying all active stocks and ETFs as of the latest trading day:
        # https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo

        #  Querying all delisted stocks and ETFs as of 2014-07-10:
        # https://www.alphavantage.co/query?function=LISTING_STATUS&date=2014-07-10&state=delisted&apikey=demo

        url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'

        # 使用 format() 方法替换字符串
        url = url.format(apikey=apikey)
        print(url)

        response = requests.get(url)


        entities = []

        # 检查响应状态码
        if response.status_code == 200:
            # 将响应内容写入文件

            # 将响应内容解码为字符串
            content = response.content.decode("utf-8")

            # 创建 CSV 读取器
            reader = csv.reader(content.splitlines())

            # 忽略表头
            next(reader, None)
            for row in reader:
                # 将数据写入数据库
                symbol, exchange, name, assetType, ipoDate, delistingDate, status = row
                entities.append(ListingStatus(symbol=symbol, exchange=exchange, name=name, assetType=assetType, ipoDate=ipoDate, delistingDate=delistingDate, status=status))

            # データ更新
            database.save_many(*entities)
        else:
            # 处理错误
            print(f"下载失败，HTTP 状态码：{response.status_code}")

    except:
        print("balance_sheet insert except:")
        traceback.print_exc()
    else:
        pass
    finally:
        pass