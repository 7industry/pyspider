#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import date

from peewee import SqliteDatabase, Model, CharField, IntegerField, DateField, BooleanField, CompositeKey, PrimaryKeyField, DecimalField
from decimal import Decimal

from config.env import db

# db = SqliteDatabase('E:/Documents/market.db')
# db.connect()
# db.create_tables([CompanyOverview, IncomeStatement])


class EquityProfile(Model):
  class Meta:
    case_sensitive = False
    database = db  # this model uses the people database
    table_name = 'equity_statistics'
    primary_key = CompositeKey('symbol')

  symbol                   = CharField()  # コード
  name                     = CharField()  # 銘柄名
  exchange                 = CharField()  # 市場区分
  established_date         = CharField()  # 設立日
  listing_date             = CharField()  # 上場日
  sector                   = CharField()  # 東証業種名 業種
  industry                 = CharField()  # 日経業種分類 業界
  dividend_yield           = DecimalField()  # 配当利回り
  ex_dividend_date         = CharField()  # 除息日
  year_change_ratio        = DecimalField(max_digits=10, decimal_places=2)  # 年初来株価上昇率
  present_price            = DecimalField()  # 現在株価
  book_value_per_share     = DecimalField()  # 1株純資産
  year_low                 = DecimalField()  # 年初来安値
  year_high                = DecimalField()  # 年初来高値
  moving_average           = DecimalField()  # 200日移動平均線
  volume                   = IntegerField()  # 出来高
  per                      = DecimalField()  # 株価収益率
  pbr                      = DecimalField()  # 株価純資産倍率
  ev_revenue               = DecimalField()  # 企业价值/收入
  ev_ebitda                = DecimalField()  # 企业价值/息税前利润
  eps                      = DecimalField()  # 基本1株当たり利益
  roa                      = DecimalField()  # 総資産利益率
  roe                      = DecimalField()  # 株主資本利益率
  debt_equity_ratio        = DecimalField()  # 债务权益比率
  own_capital_ratio        = DecimalField()  # 自己資本比率
  market_cap               = DecimalField()  # 時価総額
  enterprise_value         = DecimalField()  # 企業価値
  credit_multiplier        = DecimalField()  # 信用倍率
  grade_rating             = DecimalField()  # レーティング
  index_adoption           = CharField()  # 指数採用
  per_unit                 = CharField()  # 単元株数
  issued_shares            = CharField()  # 発行済株数
  business_scope           = CharField()  # 事業内容
  product_range            = CharField()  # 取扱い商品
  representative           = CharField()  # 代表者
  capital_stock            = CharField()  # 資本金
  address                  = CharField()  # 本社住所
  tel                      = CharField()  # 電話番号
  url                      = CharField()  # URL
  amount_of_sales          = CharField()  # 売上高
  net_income               = CharField()  # 当期純利益
  sales_cf                 = CharField()  # 営業C/F
  total_assets             = CharField()  # 総資産
  cash_and_deposits        = CharField()  # 現預金等
  total_capital            = CharField()  # 資本合計
  average_annual_income    = CharField()  # 平均年収
  delisting_date           = CharField()  # 上場廃止日
  update_date              = CharField()  # 更新日


  # 在数据保存前执行的操作
  def save(self, *args, **kwargs):
    # 验证数据
    if not self.symbol:
      raise ValueError("コード不能为空")
    # 替换 N/A 为空
    for field in self.__data__:
      if getattr(self, field) in ("N/A", "--", "---", "---倍"):
        setattr(self, field, None)
    # 将 value 转换为 Decimal 类型
    if self.year_change_ratio:
      self.year_change_ratio = self.year_change_ratio.replace(',', '').strip("%")
      self.year_change_ratio = Decimal(self.year_change_ratio) if len(self.year_change_ratio) > 0 else None
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
