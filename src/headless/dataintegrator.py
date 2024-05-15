from abc import ABC, abstractmethod
from typing import ClassVar

from src.api import database


class DataIntegrator(ABC):

  __symbol: str  # 非公開属性
  _fields: list = []  # 保護された属性

  __columns: list = ['update_date']  # 非公開属性
  __record: ClassVar['DataIntegrator'] = None # 非公開属性

  def __init__(self, entity: ClassVar['DataIntegrator']=None, symbol=None):
    if entity:
      self.__symbol = entity.__symbol
      self.__record = entity.record
      # self.__columns = self._fields + entity.columns
      self.columns = entity.columns
    if symbol:
      self.__symbol = symbol

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
  def get_company_profile(self) -> ClassVar['DataIntegrator']:
      pass


  def update(self) :
    row = self.get_company_profile()
    if self.__record is None:
      for key in row.__data__:
        if getattr(row, key) in ("N/A", "--", "---", "---倍"):
          setattr(row, key, None)
      self.__record = row
    elif row:
      for key in set(self._fields):
        if getattr(row, key) and getattr(row, key) not in ("N/A", "--", "---", "---倍"):
          setattr(self.__record, key, getattr(row, key))
    return self

  # 更新
  def save(self) -> None:
    database.update(self.__record, fields=set(self.__columns))

  # 新規
  def insert(self) -> None:
    database.save(self.__record)

if __name__ == '__main__':
  from src.headless.kabumap import Kabumap
  from src.headless.kabuyoho import Kabuyoho

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