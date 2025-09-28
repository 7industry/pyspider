#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup

html_code = '<div _ngcontent-jye-c43="" class="japanese-char inline"><ruby _ngcontent-jye-c43=""> 彼 <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">kare</p><rt _ngcontent-jye-c43="">かれ</rt></ruby><ruby _ngcontent-jye-c43=""> は <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">ha</p><rt _ngcontent-jye-c43=""></rt></ruby><ruby _ngcontent-jye-c43=""> 自分 <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">jibun</p><rt _ngcontent-jye-c43="">じぶん</rt></ruby><ruby _ngcontent-jye-c43=""> の <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">no</p><rt _ngcontent-jye-c43=""></rt></ruby><ruby _ngcontent-jye-c43=""> 違法行為 <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">ihoukoui</p><rt _ngcontent-jye-c43="">いほうこうい</rt></ruby><ruby _ngcontent-jye-c43=""> を <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">wo</p><rt _ngcontent-jye-c43=""></rt></ruby><ruby _ngcontent-jye-c43=""> 恥 <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">ha</p><rt _ngcontent-jye-c43="">は</rt></ruby><ruby _ngcontent-jye-c43=""> じていない。 <p _ngcontent-jye-c43="" ng-if="me.r" class="txt-romaji">jiteinai.</p><rt _ngcontent-jye-c43=""></rt></ruby><!----><div _ngcontent-jye-c43="" class="btn-audio inline v-align-middle"><div _ngcontent-jye-c43="" class="sprite_1 icon-18 ic_volume"></div></div></div>'

# 解析HTML
soup = BeautifulSoup(html_code, 'html.parser')

# 查找所有的<ruby>标签
ruby_tags = soup.find_all('ruby')

# 提取日语句子文本
japanese_sentences = []
for ruby in ruby_tags:
    sentence = ''.join([str(content) for content in ruby.contents if isinstance(content, str)])
    japanese_sentences.append(sentence)

# 组织成一行，并去除空格
japanese_text = ' '.join(japanese_sentences)
japanese_text = japanese_text.replace(' ', '')

# 打印日语文本
print(japanese_text)
