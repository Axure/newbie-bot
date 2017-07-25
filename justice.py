# -*- coding: utf-8 -*-
from lispy import single_repl
from path import home
import jieba
import jieba.posseg as pseg
import random


from qqbot.utf8logger import INFO

from csv import writer, reader

import re

sensitive_dict_file = home + '/.qqbot-tmp/plugins/sensitive_dict.txt'
fuck_dict_file = home + '/.qqbot-tmp/plugins/fuck_dict.txt'
political_dict_file = home + '/.qqbot-tmp/plugins/political_dict.txt'

def build_list_from_file(file_name):
    f = open(file_name, 'r')
    result_list = []
    for line in f:
        valid_line = line.rstrip()
        if valid_line != '':
            result_list.append(valid_line)
    return result_list

sensitive_list = build_list_from_file(sensitive_dict_file)
fuck_list = build_list_from_file(fuck_dict_file)
political_list = build_list_from_file(political_dict_file)

# sensitive_list = ['高神', '于神']

jieba.load_userdict('/home/zhenghu/.qqbot-tmp/plugins/dict.txt')
jieba.load_userdict(sensitive_dict_file)

def checkList(dict_list, texts, warning, is_sensitive = False):
    words = []
    tf = False
    res_sensitive = False
    for text in texts:
        for sensitive_word in dict_list:
            # print(text, type(text), sensitive_word, sensitive_word in text)
            if sensitive_word == text:
                info = '你的发言里出现了"{}"，请确认这不是'.format(sensitive_word) + warning + '行为'
                INFO(info)
                # bot.SendTo(contact, info)
                tf = True
                if is_sensitive:
                    res_sensitive = True
                    words.append('**')
                else:
                    words.append(sensitive_word)
                # pass
    res = '出现了"{}"，请确认这不是'.format(u'、'.join(words)) + warning + '行为'
    return res, tf, res_sensitive

def buildWarning(compound_list, texts, is_sensitive = False):
    overall_tf = False
    res = ''
    overall_sensitive = False
    for (dict_list, warning, is_sensitive) in compound_list:
        words, tf, words_sensitive = checkList(dict_list, texts, warning, is_sensitive)
        if tf:
            overall_tf = True
            res += words + '，'
            if words_sensitive:
                overall_sensitive = True
    return res, overall_tf, overall_sensitive

def onQQMessage(bot, contact, member, content):
    # print (type(member.qq), member.qq, member.qq == '1021542220')
    if member.qq == '1021542220':
        return
    if getattr(member, 'uin', None) == bot.conf.qq:
        INFO('你在 %s 内发言', contact)
        return
    seg_list = jieba.cut(content)
    # print(sensitive_list)
    compound_list = [(sensitive_list, '膜拜', False), (fuck_list, '不文明', False), (political_list, '敏感', True)]
    overall_message, tf, overall_sensitive = buildWarning(compound_list, list(seg_list))
    if tf:
        if overall_sensitive:
            final_message = '@{}，你的发言"{}"里{}请注意你的言行'.format(member.name, '*****', overall_message)
        else:
            final_message = '@{}，你的发言"{}"里{}请注意你的言行'.format(member.name, content, overall_message)
        INFO(final_message)
        bot.SendTo(contact, final_message)