#!/usr/bin/python3.7
# -*- coding: utf-8 -*-
# @Time  : 2019/5/29 17:44
# @Author: Jtyoui@qq.com

"""汉语拼音纠错（Chinese error correction）"""
from jtyoui.language.PinYin import load_pin_yin, chinese_to_pin_yin
from jtyoui.data import fuzzy_tone
from collections.abc import Iterable
import os


class ChineseError:
    """基于拼音谐音纠错"""

    def __init__(self, words_or_file):
        self._model = load_pin_yin(False)  # 加载拼音模型
        self._words = {}
        if (not isinstance(words_or_file, str)) and isinstance(words_or_file, Iterable):
            for word in words_or_file:
                ls = chinese_to_pin_yin(self._model, word)
                self._words[word] = ' '.join(ls)
        elif os.path.exists(words_or_file):
            with open(words_or_file, encoding='utf-8') as f:
                for line in f:
                    ls = chinese_to_pin_yin(self._model, line)
                    self._words[line] = ' '.join(ls)
        else:
            raise TypeError('输入一个纠错列表或者文件地址')
        self.fuzzy_tone = fuzzy_tone
        self._word = None

    def _flag(self, ls):
        total, index = [], -1
        value = ' '.join(ls)
        fuz = self._fuzzy(value)
        for k, v in self._words.items():
            if v in value:
                index = value.find(v)
            else:
                v = self._fuzzy(v)
                if v in fuz:
                    index = fuz.find(v)
            if index > -1:  # 替换错误单词
                index_ = value[:index].count(' ')
                name = self._word[:index_] + k + self._word[index_ + len(k):]
                total.append(name)
                index = -1
        return total

    def _fuzzy(self, words):
        """转为模糊音"""
        total = []
        for word in words.split(' '):
            for correct, error in self.fuzzy_tone.items():
                if error not in word and correct in word:
                    word = word.replace(correct, error)
            total.append(word)
        return ' '.join(total)

    def error_word(self, word):
        """将错误的词语转为正确的词语"""
        ls = chinese_to_pin_yin(self._model, word)
        self._word = word
        total = self._flag(ls)
        return total


if __name__ == '__main__':
    ce = ChineseError(['六盘水钟山区'])
    print(ce.error_word('我在六盘谁中三区里面'))
