#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import date

from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField, BooleanField, CompositeKey, \
  PrimaryKeyField, DecimalField
from decimal import Decimal

from src.config.env import db

# db = SqliteDatabase('E:/Documents/market.db')
# db.connect()
# db.create_tables([CompanyOverview, IncomeStatement])


class CompanyProfile(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    table_name = 'company_profile'
    primary_key = CompositeKey('symbol')

  symbol                   = CharField()  # コード
  spotlight                = CharField()  # 注目度
  name                     = CharField()  # 企業名
  sector                   = CharField()  # 業種 東証業種名
  industry                 = CharField()  # 業界 日経業種分類
  exchange                 = CharField()  # 上場市場
  amount_of_sales          = CharField()  # 売上高
  net_income               = CharField()  # 当期純利益
  sales_cf                 = CharField()  # 営業C/F
  total_assets             = CharField()  # 総資産
  cash_and_deposits        = CharField()  # 現預金等
  total_capital            = CharField()  # 資本合計
  average_annual_income    = CharField()  # 平均年収
  established_date         = CharField()  # 設立年月日
  index_adoption           = CharField()  # 指数採用
  url                      = CharField()  # URL
  representative           = CharField()  # 代表者
  listing_date             = CharField()  # 上場年月日
  per_unit                 = CharField()  # 単元株数
  capital_stock            = CharField()  # 資本金
  address                  = CharField()  # 本社住所
  tel                      = CharField()  # 電話番号
  dividend_yield           = CharField()  # 配当利回り
  per                      = CharField()  # PE Ratio (TTM)
  pbr                      = CharField()  # 市净率
  eps                      = CharField()  # 每股收益  (TTM)
  roa                      = CharField()  # ROA
  roe                      = CharField()  # ROE股东权益回报率
  debt_equity_ratio        = CharField()  # 债务权益比率
  own_capital_ratio        = CharField()  # 自己資本比率
  market_cap               = CharField()  # 時価総額(百万円)
  enterprise_value         = CharField()  # 企業価値
  book_value_per_share     = CharField()  # 1株純資産
  year_high                = CharField()  # 年高値
  year_low                 = CharField()  # 年安値
  year_change_ratio        = DecimalField(max_digits=10, decimal_places=2)  # 年初来株価上昇率
  moving_average_deviation = CharField()  # 200日移動平均乖離率
  grade_rating             = CharField()  # レーティング 「评级」「等级」
  credit_multiplier        = CharField()  # 信用倍率(倍)
  ex_dividend_date         = CharField()  # 除息日
  business_scope           = CharField()  # 事業内容
  product_range            = CharField()  # 取扱い商品
  update_date              = CharField()  # 更新日

  # 在数据保存前执行的操作
  def save(self, *args, **kwargs):
    # 替换 N/A 为空
    for field in self.__data__:
      if getattr(self, field) in ("N/A", "--", "---", "---倍"):
        setattr(self, field, None)
    # 将日期转换为字符串
    self.update_date = date.today().strftime('%Y%m%d')
    # 将 value 转换为 Decimal 类型
    if self.year_change_ratio:
      self.year_change_ratio = self.year_change_ratio.replace(',', '').strip("%")
      self.year_change_ratio = Decimal(self.year_change_ratio) if len(self.year_change_ratio) > 0 else None
    # # 验证数据
    # if not self.name:
    #   raise ValueError("名称不能为空")
    super().save(*args, **kwargs)



  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class ListingStatus(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'exchange')

  symbol = CharField()
  exchange = CharField()
  name = CharField()
  assetType = CharField()
  ipoDate = DateField()
  delistingDate = DateField()
  status = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class IPOCalendar(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'exchange')

  symbol = CharField()
  name = CharField()
  ipoDate = DateField()
  priceRangeLow = DecimalField()
  priceRangeHigh = DecimalField()
  currency = CharField()
  exchange = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class EarningsCalendar(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('symbol', 'fiscalDateEnding')

  symbol = CharField()
  name = CharField()
  reportDate = DateField()
  fiscalDateEnding = DateField()
  estimate = DecimalField()
  currency = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class CompanyOverview(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database

  Symbol = PrimaryKeyField()
  AssetType = CharField()
  Name = CharField()
  Description = CharField()
  CIK = CharField()
  Exchange = CharField()
  Currency = CharField()
  Country = CharField()
  Sector = CharField()
  Industry = CharField()
  Address = CharField()
  FiscalYearEnd = CharField()
  LatestQuarter = CharField()
  MarketCapitalization = CharField()
  EBITDA = CharField()
  PERatio = CharField()
  PEGRatio = CharField()
  BookValue = CharField()
  DividendPerShare = CharField()
  DividendYield = CharField()
  EPS = CharField()
  RevenuePerShareTTM = CharField()
  ProfitMargin = CharField()
  OperatingMarginTTM = CharField()
  ReturnOnAssetsTTM = CharField()
  ReturnOnEquityTTM = CharField()
  RevenueTTM = CharField()
  GrossProfitTTM = CharField()
  DilutedEPSTTM = CharField()
  QuarterlyEarningsGrowthYOY = CharField()
  QuarterlyRevenueGrowthYOY = CharField()
  AnalystTargetPrice = CharField()
  AnalystRatingStrongBuy = CharField()
  AnalystRatingBuy = CharField()
  AnalystRatingHold = CharField()
  AnalystRatingSell = CharField()
  AnalystRatingStrongSell = CharField()
  TrailingPE = CharField()
  ForwardPE = CharField()
  PriceToSalesRatioTTM = CharField()
  PriceToBookRatio = CharField()
  EVToRevenue = CharField()
  EVToEBITDA = CharField()
  Beta = CharField()
  High52Week = CharField()
  Low52Week = CharField()
  MovingAverage50Day = CharField()
  MovingAverage200Day = CharField()
  SharesOutstanding = CharField()
  DividendDate = CharField()
  ExDividendDate = CharField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data,
      High52Week=json_data["52WeekHigh"],
      Low52Week=json_data["52WeekLow"],
      MovingAverage50Day=json_data["50DayMovingAverage"],
      MovingAverage200Day=json_data["200DayMovingAverage"],
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
      # "52WeekHigh": self.High52Week,
      # "52WeekLow": self.Low52Week,
    }


class IncomeStatement(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  grossProfit = IntegerField()
  totalRevenue = IntegerField()
  costOfRevenue = IntegerField()
  costofGoodsAndServicesSold = IntegerField()
  operatingIncome = IntegerField()
  sellingGeneralAndAdministrative = IntegerField()
  researchAndDevelopment = IntegerField()
  operatingExpenses = IntegerField()
  investmentIncomeNet = CharField()
  netInterestIncome = IntegerField()
  interestIncome = CharField()
  interestExpense = IntegerField()
  nonInterestIncome = CharField()
  otherNonOperatingIncome = IntegerField()
  depreciation = IntegerField()
  depreciationAndAmortization = IntegerField()
  incomeBeforeTax = IntegerField()
  incomeTaxExpense = IntegerField()
  interestAndDebtExpense = IntegerField()
  netIncomeFromContinuingOperations = IntegerField()
  comprehensiveIncomeNetOfTax = IntegerField()
  ebit = IntegerField()
  ebitda = IntegerField()
  netIncome = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class BalanceSheet(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  totalAssets = IntegerField()
  totalCurrentAssets = IntegerField()
  cashAndCashEquivalentsAtCarryingValue = IntegerField()
  cashAndShortTermInvestments = IntegerField()
  inventory = IntegerField()
  currentNetReceivables = CharField()
  totalNonCurrentAssets = IntegerField()
  propertyPlantEquipment = IntegerField()
  accumulatedDepreciationAmortizationPPE = CharField()
  intangibleAssets = IntegerField()
  intangibleAssetsExcludingGoodwill = IntegerField()
  goodwill = IntegerField()
  investments = CharField()
  longTermInvestments = CharField()
  shortTermInvestments = IntegerField()
  otherCurrentAssets = IntegerField()
  otherNonCurrentAssets = CharField()
  totalLiabilities = IntegerField()
  totalCurrentLiabilities = IntegerField()
  currentAccountsPayable = IntegerField()
  deferredRevenue = CharField()
  currentDebt = IntegerField()
  shortTermDebt = IntegerField()
  totalNonCurrentLiabilities = IntegerField()
  capitalLeaseObligations = CharField()
  longTermDebt = IntegerField()
  currentLongTermDebt = CharField()
  longTermDebtNoncurrent = CharField()
  shortLongTermDebtTotal = IntegerField()
  otherCurrentLiabilities = IntegerField()
  otherNonCurrentLiabilities = IntegerField()
  totalShareholderEquity = IntegerField()
  treasuryStock = IntegerField()
  retainedEarnings = IntegerField()
  commonStock = IntegerField()
  commonStockSharesOutstanding = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class CashFlow(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedCurrency = CharField()
  operatingCashflow = IntegerField()
  paymentsForOperatingActivities = IntegerField()
  proceedsFromOperatingActivities = CharField()
  changeInOperatingLiabilities = IntegerField()
  changeInOperatingAssets = IntegerField()
  depreciationDepletionAndAmortization = IntegerField()
  capitalExpenditures = IntegerField()
  changeInReceivables = IntegerField()
  changeInInventory = IntegerField()
  profitLoss = IntegerField()
  cashflowFromInvestment = IntegerField()
  cashflowFromFinancing = IntegerField()
  proceedsFromRepaymentsOfShortTermDebt = IntegerField()
  paymentsForRepurchaseOfCommonStock = CharField()
  paymentsForRepurchaseOfEquity = CharField()
  paymentsForRepurchaseOfPreferredStock = CharField()
  dividendPayout = IntegerField()
  dividendPayoutCommonStock = IntegerField()
  dividendPayoutPreferredStock = CharField()
  proceedsFromIssuanceOfCommonStock = CharField()
  proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet = IntegerField()
  proceedsFromIssuanceOfPreferredStock = CharField()
  proceedsFromRepurchaseOfEquity = IntegerField()
  proceedsFromSaleOfTreasuryStock = CharField()
  changeInCashAndCashEquivalents = CharField()
  changeInExchangeRate = CharField()
  netIncome = IntegerField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }


class Earnings(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    primary_key = CompositeKey('Symbol', 'ReportType', 'fiscalDateEnding')

  Symbol = CharField()
  ReportType = CharField()
  fiscalDateEnding = DateField()
  reportedDate = DateField()
  reportedEPS = DecimalField()
  estimatedEPS = DecimalField()
  surprise = DecimalField()
  surprisePercentage = DecimalField()

  # 指定反序列化时要使用的字段　属性名が不一致に対応
  @classmethod
  def from_json(cls, json_data):
    return cls(
      **json_data
    )

  # 指定字段名和 JSON key 的对应关系
  def to_json(self):
    return {
      **self.__data__,
    }
