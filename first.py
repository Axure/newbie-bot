# -*- coding: utf-8 -*-
from lispy import single_repl
from path import home

import jieba
import jieba.posseg as pseg
import random


from thesarus import thesarus

import re

def process_sentences(s):
    # sentences = re.split(u'。|？|！|，', s)
    sentences = [s]

    dictionary = dict()

    def get_word_according_to_type(type):
        random_key = random.choice(list(dictionary[type].keys()))
        if dictionary[type][random_key] == 1:
            dictionary[type].pop(random_key, None)
        else:
            dictionary[type][random_key] -= 1
        return random_key

    i = 0
    sentence_grammar = dict()
    for sp in sentences:
        seg_list = jieba.cut(sp, cut_all=False)
        print("/ ".join(seg_list))
        seg_list_with_type = jieba.posseg.cut(sp)
        sentence_grammar[i] = []
        for w in seg_list_with_type:
            print(w.word, w.flag)
            sentence_grammar[i].append(w.flag)
            if not(w.flag in dictionary):
                print("fuck")
                dictionary[w.flag] = dict()
            if not(w.word in dictionary[w.flag]):
                dictionary[w.flag][w.word] = 0
            dictionary[w.flag][w.word] += 1
        i += 1

    for flag in dictionary:
        # print(flag, ":", "/ ".join(dictionary[flag]))
        print(flag, ": ")
        for words in dictionary[flag]:
            print("[", words.encode('utf-8'), dictionary[flag][words], "], ",)
        print("")

    for grammars in sentence_grammar:
        print("/".join(sentence_grammar[grammars]))

    res = ''
    for grammars in sentence_grammar:
        temp_sentence = ""
        for grammar in sentence_grammar[grammars]:
            temp_sentence += get_word_according_to_type(grammar)
        # print(temp_sentence)
        res += temp_sentence
    return res

def public_props(obj):
    return (name for name in dir(obj) if not name.startswith('_'))


messages = ["你想說啥？"] + thesarus
max_size = 1000

jieba.load_userdict(home + '/.qqbot-tmp/plugins/dict.txt')

def buildMessage(max_size):
    count = int(max_size * random.random()) + 1
    res = ''
    for i in range(count):
        size = len(messages)
        id = int(size * random.random())
        if id == size:
            id -= 1
        print(id, messages)
        res += messages[id] + ' '
    return res

def onQQMessage(bot, contact, member, content):
    if member.qq == '1021542220':
        return
    if content == '/hello':
        bot.SendTo(contact, member.name + '你好，我是你大爺')
    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
    elif content[:4] == '/who':
       # bot.SendTo(contact, content)
        #bot.SendTo(contact, single_repl(content))
        res = ''

        for key in public_props(member):
            value = getattr(member, key)
#            res = res + str(attr) + "\n"
            res = res + str(key) + ': ' + str(value) + "\n"
        bot.SendTo(contact, res)
    elif content[:5] == '/talk':
        bot.SendTo(contact, "@" + member.name + " " + buildMessage(5))
    elif content[:5] == '/lisp':
        bot.SendTo(contact, "@" +  member.name + ": " + single_repl(content[5:].strip()))
    elif content[:7] == '/python':
        bot.SendTo(contact, "@" +  member.name + ": " + str(eval(content[5:].strip())) )
    elif content[:9] == '/pointer?':
        bot.SendTo(contact, member.name + "你好，你問我指針是誰？指針是zq的老公，是一個很老的學長。")
        return
    elif content[:8] == '/pointer':
        bot.SendTo(contact, member.name + "你好，我是指針，我的老婆是zq。")
        return
    elif content[:4] == '/zq?':
        bot.SendTo(contact, member.name + "，你問我zq是誰？zq是一個可愛的學姐。")
    elif content[:4] == '/蹭一蹭':
        bot.SendTo(contact, member.name + "你好，我是指針，我的老婆是zq。你確定要蹭我嗎？")
    elif content[:4] == '/faq':
        bot.SendTo(contact, """我是常見問題和解答：
Q：工信在哪个校区？
A：工信大类大一大二在紫金港，之后迁到玉泉。
Q：学校有哪些快递点？哪里可以取快递？
A：京东和顺丰的快递点在北街，其他快递基本都由菜鸟驿站代理。
Q：新生要带电脑吗？
A：建议带，否则会不方便。机房的电脑还是不如自己的电脑。
Q：工信对电脑要求高吗？
A：打游戏的要求高，不打的话能跑的动程序就可以。如果还想进一步咨询的话建议附上日常需求预算及对配置、外观等其他要求在群里提问（有空也可以看看关于选购电脑的群文件）。
（在预算范围内往好里挑，别去实体店买电脑！
Q：开学前要预习什么？
A：放假就好好玩学什么习（可以先看一遍道德经（不是
如果真心想静下心来学习，想提前预习大学课程的可以结合培养方案学一下一些基础数学课和专业课程，比如微积分线代c程；想学习专业知识的可以根据自己的情况直接学一些专业性的内容。（虽然感觉这条建议说了跟没说一样
Q：工信一届几个班？
A：25-30不等。
Q：哪个专业比较好？
A：不管哪个专业都是好专业。如果还没有什么具体兴趣倾向欢迎来进行人生相谈（逃
        """)
    elif content[:5] == '/help':
        bot.SendTo(contact, """
/help 幫助
/faq 新生常見問題
/talk 和我說話
/pointer? 瞭解指針的故事
/mix <text> 胡言亂語
/lisp <code> 執行 Lisp 代碼""")
    elif content[:6] == '/jieba':
        seg_list = jieba.cut(content[6:].strip())
        res = " ".join(seg_list)
        bot.SendTo(contact, res)
    elif content[:4] == '/mix':
        res = process_sentences(content[4:].strip())
        bot.SendTo(contact, res)
    elif content[:8] == '/welcome':
        bot.SendTo(contact, '歡迎' + content[8:].strip())
    else:
        true_content = content.strip()
        if true_content != '':
            messages.append(true_content)
   # else:
    #    bot.SendTo(contact, content)
