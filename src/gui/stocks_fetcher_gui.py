#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from tkinter import StringVar, LabelFrame, Label, Entry, Button, Text, Tk
from tkinter.constants import W, NONE, END
import tkinter.filedialog
import tkinter.messagebox

from src.headless.kabumap import Kabumap
from src.headless.kabuyoho import Kabuyoho
from src.headless.minkabu import Minkabu
from src.headless.nikkei import Nikkei
from src.headless.price_change_ranking import Kabuka
from src.headless.yahoo import Yahoo

class FetcherGui():

  def __init__(self, init_window_name):
    self.init_window_name = init_window_name
    
    # コード
    self.symbol = StringVar()
    
    # SQLite File Path
    self.db_file_path = StringVar()
    
    # 保存文件名
    self.save_name = StringVar()
    
    # cookie
    self.cookie = StringVar()

    # 将控制台输出重定向到Tkinter
    sys.stdout = self

  # 控制台输出
  def write(self, message):
    self.text.insert(END, str(message))
    self.text.see(END)
    self.text.update()

    
  # 设置窗口
  def set_init_window(self):
    self.init_window_name.title("股票数据下载工具")
    self.init_window_name.geometry('+500+200')
    
    input_frame = LabelFrame(text="配置")
    input_frame.grid(column=0, row=0, padx=5, pady=5)
    
    Label(input_frame, text="商品代码：").grid(row=0, column=0, sticky=W)
    symbol_label = Entry(input_frame, width=100, textvariable=self.symbol)
    symbol_label.insert('0', '4755')
    symbol_label.grid(row=0, column=1, columnspan=2, sticky=W)
    
    Label(input_frame, text="数据文件：").grid(row=1, column=0, sticky=W)
    file_label = Entry(input_frame, width=50, textvariable=self.db_file_path)
    file_label.grid(row=1, column=1, columnspan=2, sticky=W)
    file_label.insert('0', os.path.expanduser('~') + "/market.db")
    Button(input_frame, text="浏览", command=self.select_data_file).grid(row=1, column=2, sticky=W)
    
    Label(input_frame, text="ランキング：").grid(row=2, column=0, sticky=W)
    kikubon = Entry(input_frame, width=50, textvariable=self.save_name)
    kikubon.insert('0', 'https://www.kabuka.jp.net/neagari-nesagari.html')
    kikubon.config(state='readonly')
    kikubon.grid(row=2, column=1, columnspan=2, sticky=W)
    Button(input_frame, text="ランキング下载", command=self.ranking_down).grid(row=2, column=2, sticky=W)
    
    Label(input_frame, text="Cookie：").grid(row=3, column=0, sticky=W)
    # wrap属性是指 自动换行。WORD表示单词换行；CHAR(default)表示字符换行;NONE 表示不自动换行
    self.cookie_text = Text(input_frame, width=100, height=4)
    self.cookie_text.insert('1.0', 'kikubonses=ggm3ijialp7up1van8i9lj5sim; login20160719=a4c8940220d0e0cea851043aec67f4b9e44c22c4; __c__login20160719=d41123a6e04fd28ae8a7bf2ccb6fcd22e38b2066; browsingData=["720"]; cookieconsent_status=deny')
    self.cookie_text.grid(row=3, column=1, columnspan=2, sticky=W) 
    
    action_frame = LabelFrame()
    action_frame.grid(row=1, column=0, padx=0, pady=0)
    
    Button(action_frame, text="开始下载", command=self.download).grid(row=0, column=0)
    
    self.text = Text(action_frame, width=100, height=40, wrap=NONE)
    self.text.grid(row=1, column=0, sticky=W)

  
  # 选择保存的SQLite数据文件
  def select_data_file(self):
    filename = tkinter.filedialog.askopenfilename()
    # fodername = tkinter.filedialog.askdirectory()
    self.db_file_path.set(filename)
  
  # 开始下载
  def ranking_down(self):
    Kabuka.update_company_profile()



  # 开始下载
  def download(self):
    self.cookie = self.cookie_text.get("1.0", END)
    db_path = self.db_file_path.get()
    file_name = self.save_name.get()

    symbol = self.symbol.get().strip()
    print(f"symbol：{symbol} start...")

    Kabumap.update_company_profile(symbol)
    Nikkei.update_company_profile(symbol)
    Kabuyoho.update_company_profile(symbol)
    Minkabu.update_company_profile(symbol)
    Yahoo.update_company_profile(symbol)
    print(f"symbol：{symbol} end!")
    
def gui_start():
  init_window = Tk()
  ui = FetcherGui(init_window)
  ui.set_init_window()
  
  init_window.mainloop()

  
gui_start()
