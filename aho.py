#!/usr/bin/env python
# coding: utf-8
# author: nemo_chen
import ahocorasick
A = ahocorasick.Automaton()
titles = ['Hello Kitty3色蔬菜细面300克 婴儿幼儿营养面条宝宝辅食面条']
word_dict = {}
with open('categories.csv', 'r') as f:
        for line in f.readlines():
                    line = line.strip()
                            word_key = line.split(':')[0]
                                    word_value = list(line.split(':')[1].split('|'))
                                            word_dict[word_key] = word_value
                                                    line = (line.split(':')[1].split('|'))
                                                            for word in line:
                                                                            if word == "":
                                                                                                continue
                                                                                                        A.add_word(word, word)
                                                                                                        A.make_automaton()
                                                                                                        for title in titles:
                                                                                                                category = []
                                                                                                                    aa = A.iter(title)
                                                                                                                        ret = []
                                                                                                                            matches = {}
                                                                                                                                for (k,v) in aa:
                                                                                                                                            matches[v] = 1
                                                                                                                                                for (k,v) in matches.items():
                                                                                                                                                            ret.append(k)
                                                                                                                                                                for value in word_dict.items():
                                                                                                                                                                            if ret[0] in value[1]:
                                                                                                                                                                                            category.append(value[0]) #关键字太多，所以写死了一个keyword匹配的结果
                                                                                                                                                                                                        #print(ret[0], value[0], value[1]) 
                                                                                                                                                                                                            print(category[0])
