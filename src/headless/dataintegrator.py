import re
from abc import ABC, abstractmethod
from typing import ClassVar

from peewee import IntegerField, FloatField, DecimalField, CharField

from api import database


class DataIntegrator(ABC):
  __symbol: str  # 非公開属性
  _fields: list = []  # 保護された属性

  __columns: list = ['update_date']  # 非公開属性
  __record: ClassVar['DataIntegrator'] = None  # 非公開属性

  def __init__(self, entity: ClassVar['DataIntegrator'] = None, symbol=None):
    if entity:
      self.__symbol = entity.__symbol
      self.__record = entity.record
      self.columns = entity.columns
    if symbol:
      self.__symbol = symbol
      self.__columns = self.__columns + self._fields

  @property
  def symbol(self):
    return self.__symbol

  @property
  def fields(self):
    return self._fields

  @property
  def record(self):
    return self.__record

  @property
  def columns(self):
    return self.__columns

  @columns.setter
  def columns(self, columns: list):
    self.__columns = self._fields + columns

  @abstractmethod
  def get_equity_statistics(self) -> ClassVar['DataIntegrator']:
    pass

  def update(self):
    row = self.get_equity_statistics()

    # 遍历字段名和对应的值
    for field_name, field_type in row._meta.fields.items():
      value = getattr(row, field_name)
      # 字符串去杂
      if value in ("N/A", "--", "---", "---倍"):
        value = None
      elif value and isinstance(field_type, (IntegerField, FloatField, DecimalField)):
        # 数值计算
        value = self.convert_number_unit(value)
        setattr(row, field_name, value)
        # print(f"{field_name} = {value}")
      # elif isinstance(field_type, CharField):
      #   # 字符串去杂
      #   if value in ("N/A", "--", "---", "---倍"):
      #     print(f"{field_name} = {value}")
      #     value = None

    if self.__record is None:
      self.__record = row
    elif row:
      for key in set(self._fields):
        if getattr(row, key):
          setattr(self.__record, key, getattr(row, key))

    return self

  # 更新
  def save(self) -> None:
    database.update(self.__record, fields=set(self.__columns))

  # 新規
  def insert(self) -> None:
    database.save(self.__record)

  # 数字の単位を変換する
  @staticmethod
  def convert_number_unit(decoded_str: str) -> str:
    # 去除括号中的时间格式 (hh:mm)
    cleaned_str  = re.sub(r'\(\d{1,2}:\d{2}\)', '', decoded_str)
    # 正则表达式匹配：符号、数字、单位
    pattern = r'([-+])?(\d+(?:,\d+)*(?:\.?\d+)?)\s*([^\d\s]+)?'
    matches = re.findall(pattern, cleaned_str)

    sign = 1
    total = 0.0

    for i, match in enumerate(matches):
      symbol, value_str, units = match

      # 判断符号
      if i == 0 and symbol == '-':
        sign = -1

      # 去除逗号并转换为浮点数
      number = float(value_str.replace(',', ''))

      # 计算单位倍数
      multipliers = 1
      if units:
        for unit in units:
          if unit == '十':
            multiple = 10
          elif unit == '百':
            multiple = 100
          elif unit == '千':
            multiple = 1000
          elif unit == '万':
            multiple = 10000
          elif unit == '億':
            multiple = 100000000
          elif unit == '兆':
            multiple = 1000000000000
          elif unit == 'K':
            multiple = 1000
          elif unit == 'M':
            multiple = 1000000
          elif unit == 'B':
            multiple = 1000000000
          elif unit == 'T':
            multiple = 1000000000000
          else:
            multiple = 1
          multipliers *= multiple

      total += number * multipliers

    total *= sign

    if total.is_integer():
      total = int(total)

    return str(total)


if __name__ == '__main__':
  from headless.kabumap import Kabumap
  from headless.kabuyoho import Kabuyoho

  # Create an instance of the Dog class
  baseData: 'DataIntegrator' = Kabuyoho(symbol="7203")
  baseData.update()

  baseData = Kabumap(baseData)
  baseData.update()

  baseData.save()

  # print(dog.record)
  # dog.record = Dog("dog1")
  # print(dog.record)

  # cat = Cat("Fido")
  # print(cat.record)
  # cat.record = Cat("cat2")
  # print(cat.record)
