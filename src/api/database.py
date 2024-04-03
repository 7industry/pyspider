#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import traceback

from src.config.env import db
from peewee import DoesNotExist


# 插入单条数据
# model = CompanyOverview(Symbol='IBM1', AssetType='22313', Name='B1ob')
# model.save(force_insert=True)
def save(modle):
  try:
    modle.save(force_insert=True)
  except:
    # traceback.print_exc()
    raise ValueError("database insert except:")
  else:
    return True
  finally:
    pass


# 批量插入数据
def insert_many(*entities):
  try:
    with db.transaction():
      # 插入数据
      for entity in entities:
        entity.save(force_insert=True)
      db.commit()
  except:
    db.rollback()
    # traceback.print_exc()
    raise ValueError("database insert except:")
  else:
    return True
  finally:
    pass


# createでINSERTする
# grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
def insert(model_class, **json_dcit):
  try:
    model_class.create(**json_dcit)
  except:
    # traceback.print_exc()
    raise ValueError("database insert except:")
  else:
    return True
  finally:
    pass


def update(model_class, json_dcit, fields=None):
  try:
    # save()方法会检查模型实例是否存在主键。如果存在，则执行UPDATE操作更新现有行
    #   only 参数用于指定要更新的字段 model.save(only=['name', 'age'])
    model_class(**json_dcit).save(only=fields)
  except:
    print("database update except:")
    traceback.print_exc()
  else:
    return True
  finally:
    pass


def update(entity, fields=None):
  try:
    # save()方法会检查模型实例是否存在主键。如果存在，则执行UPDATE操作更新现有行
    #   only 参数用于指定要更新的字段 model.save(only=['name', 'age'])
    entity.save(only=fields)
  except:
    print("database update except:")
    traceback.print_exc()
  else:
    return True
  finally:
    pass


# 批量插入或更新数据
# ListingStatus.get_by_id((symbol == symbol) & (exchange == exchange))
def save_many(*entities):
  try:
    with db.transaction():
      for entity in entities:

        query = entity.select()
        #  primary_key 字段名
        for field in entity._meta.primary_key.field_names:
          query = query.where(getattr(type(entity), field) == getattr(entity, field))

        try:
          query.get()
        except DoesNotExist:
          # increat
          entity.save(force_insert=True)
        else:
          query = entity.select()
          #  全字段名
          for field in entity.__data__.keys():
            query = query.where(getattr(type(entity), field) == getattr(entity, field))

          try:
            query.get()
          except DoesNotExist:
            # update
            entity.save()

      db.commit()
  except:
    db.rollback()
    # traceback.print_exc()
    raise ValueError("database insert except:")
  else:
    return True
  finally:
    pass


# 根据主键删除
def delete(model_class, id):
  try:
    # model_class.delete().where(**json_dcit)
    model_class.delete().where(getattr(model_class, model_class._meta.primary_key.field_names[0]) == id).execute()
  except:
    print("database delete except:")
    traceback.print_exc()
  else:
    return True
  finally:
    pass


# 查询数据 TODO
# ListingStatus.get_by_id((symbol == symbol) & (exchange == exchange))
def find(model_class, json_dcit):
  try:
    entity = model_class.select().where(getattr(model_class, model_class._meta.primary_key.field_names[0]) == id).execute()
    # entity = model_class.select().where(CompanyProfile.symbol == id).execute()
  except:
    print("database update except:")
    traceback.print_exc()
  else:
    return True
  finally:
    pass

if __name__ == '__main__':
  from peewee import SqliteDatabase, Model, CharField, DateField, BooleanField, ForeignKeyField, IntegrityError
  from datetime import date

  # db = SqliteDatabase(':memory:')
  db = SqliteDatabase('I:/sqlite/market.db')
  # db = SqliteDatabase('E:/Documents/market.db')
  db.connect()


  class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
      database = db  # This model uses the "people.db" database.


  class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
      database = db  # this model uses the people database


  try:
    db.create_tables([Person, Pet])
    with db.transaction():
      # オブジェクトを作ってSaveすることでINSERTする
      uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
      uncle_bob.save(True)  # bob is now stored in the database

      # createでINSERTする
      grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
      herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)

      bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
      herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
      herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
      herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

      print("全部取得-----------------")
      for person in Person.select():
        print(person.name, person.is_relative)

      print("catのみ取得-----------------")
      query = Pet.select().where(Pet.animal_type == 'cat')
      for pet in query:
        print(pet.name, pet.owner.name)

      print("Joinの例-----------------")
      query = (Pet
               .select(Pet, Person)
               .join(Person)
               .where(Pet.animal_type == 'cat'))
      for pet in query:
        print(pet.name, pet.owner.name)

      print("更新の例-----------------")
      update_pet = Pet.get(Pet.name == 'Kitty')
      update_pet.name = 'Kitty(updated)'
      update_pet.save()

      query = (Pet
               .select(Pet, Person)
               .join(Person)
               .where(Pet.animal_type == 'cat'))
      for pet in query:
        print(pet.name, pet.owner.name)

      print("削除の例-----------------")
      del_pet = Pet.get(Pet.name == 'Mittens Jr')
      del_pet.delete_instance()

      query = (Pet
               .select(Pet, Person)
               .join(Person)
               .where(Pet.animal_type == 'cat'))
      for pet in query:
        print(pet.name, pet.owner.name)

      db.commit()


  except IntegrityError as ex:
    print(ex)
    db.rollback()
  finally:
    db.close()
