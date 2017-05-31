# -*- coding: utf-8 -*-
from __future__ import division
import aiml
import sys
import jieba
import math
# import SVMClass
jieba.load_userdict("./res/negative_word.txt")
reload(sys)


#全局变量cnt_neg用于记录负面词汇出现的次数，在此处初始化
#cnt_sum记录输入的条数
#p_neg记录负面词汇出现次数/输入总条数
cnt_neg = 0
cnt_sum = 0
p_neg = 0.0

class ChatRobot:
    def __init__(self):
        self.negative_word_path = "./res/negative.txt"



        # SVM
        # self.SVM = SVMClass.SVM()
        # print self.SVM.test("我好累")

        #不加这个就不能用cmp9()
        sys.setdefaultencoding('utf8')

        #加载aiml文件
        self.kernel = aiml.Kernel()
        self.kernel.learn("std_startup.xml")
        self.kernel.respond("load aiml b")


        #Mycut函数对输入进行分词，利用jieba的第三方库
    def Mycut(self, str):
        #jieba进行分词
        seg = jieba.cut(str)
        seg_1 = jieba.cut(str)

        #对分词结果遍历
        self.Mycount(seg_1)

        #返回原句以传入kernel
        return "".join(seg)

        #Mycount函数用来记录负面词汇个数
    def Mycount(self, seg):
        #cnt_neg为记录负面词汇的全局变量
        global cnt_neg
        global cnt_sum

        #读取负面词汇文件
        file = open(self.negative_word_path)
        lines = file.readlines()
        #遍历
        for s in seg:
            for line in lines:
        #		print s ,line
                #如果词汇为负面词汇，cnt_neg++
                if cmp(s,(line.strip())) == 0:
                    cnt_neg +=1
        #print "count"
        cnt_sum += 1
        return


    def chat(self, question):
        usr_input = question

        #如果输入是exit则退出程序
        if usr_input == "exit":
            p_neg = cnt_neg/(cnt_sum-1)

            if p_neg > 0.5:
               print r'''
        你好像有点不开心，去和咱们的老师聊聊，怎么样
        如果你在中关村校区，可以在周一至周五的14:00-17:00和周一至周四的18:30-21:30打68913687预约
        如果在良乡校区的话，可以在周一至周五的09:00-12:00和13:00-16:00打81384940预约～
        相信和老师聊聊的你会舒坦一些～
                    '''

            exit()

        #调用Mycut()，对输入进行分词
        cut_output = self.Mycut(usr_input)
        #输出结果
        #print cut_output
        answer = self.kernel.respond(cut_output)
        #如果没有答案，则添加用户的回答
        if answer is "":
            print "No Answer for -> \"" +question+"\""
            return ""

        return answer

    def addAnswer(self, question,new_answer):

        #用户教的回答都存在new_answer.aiml里
        fp = file('./res/new_answer.aiml')
        s = fp.read()
        fp.close()
        #将文档以一行为单位切开
        split_line = s.split('\n')
        #每次都在文档的第5行和第6行插入
        split_line.insert(5,"<category><pattern>"+question+"</pattern>")
        split_line.insert(6,"<template>"+new_answer+"</template>\n</category>\n")
        s = '\n'.join(split_line)
        #把加入新答案的内容写回文档里
        fp = file('./res/new_answer.aiml','w')
        fp.write(s)
        fp.close()

        #重新加载new_answer.aiml文档
        self.kernel.respond("load aiml b")
        print "添加成功，试试再问我一遍：）"
