#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from model.SchemaModel import CompanyOverview
from api import database
from api import alphavantage

# reloadium.start()

# data = alphavantage.company_overview("GOOG")
# data = alphavantage.income_statement("GOOG")
# data = alphavantage.balance_sheet("GOOG")
# data = alphavantage.cash_flow("GOOG")

# data = alphavantage.earnings("GOOG")

data = alphavantage.listing_status()


# SchemaModel.update(data)

# 使用 CompanyOverview 类名
# database.delete(CompanyOverview, data)

# 将 JSON 格式字符串转换为 Peewee 模型对象
# model = CompanyOverview.from_json(json)
# CompanyOverview.save(model)

# 将字典转换为键值对元组的列表
# items = dict({'Symbol': 'GOOG', 'AssetType': 'Common Stock'})

# 去除 key 引号
# data = {key.replace("'", ''): value for key, value in json_dcit.items()}

# items = dict(json_dcit)
# items = dict({'Symbol': 'GOOG', 'AssetType': 'Common Stock'})
# items = json_dcit.items()

