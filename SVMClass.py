# -*- coding:utf-8 -*-

from sklearn import svm
import jieba
import numpy as np
import random
'''
SVM方法
1，通过词库建立词典： key-value 形式，key是单词、value是其对应的下标
2，训练： 对于训练词库，将每句话变为[0，0，1...0，1]形式，并且将其下标标出
3，      将其放入SVM进行训练
4，测试： 将测试语句根据词典变成向量形式，并放入SVM中，获得结果即可

比如：
   我们的语料库中有共有10个单词，那么我们需要建立1*10的向量。
   [吃饭，今天，你，了，树木，我，爱，吗，喜欢，书包]
   也就是说，我们所有的话由这10个单词组成。

   对于一句话：你今天吃饭了吗 --> [1，1，1，1，0，0，0，1，0，0]，其中1代表出现，0 代表不出现

   对于我们的语料库，需要包含汉语的大多数词汇，所以是一个近似1*40000的向量。
   经过向量化之后，就可以通过SVM对向量进行分类了，也就是对文本进行分类。
'''


class SVM:
    def __init__(self, words_path="./res/WordDataset_try.txt", positive_path="./res/try_positive.txt", negative_path = "./res/try_negative.txt"):
        self.words_path = words_path
        self.positive_path = positive_path
        self.negative_path = negative_path

        '''
        1，读入语料库，并且建立 key-value 形式
        '''
        self.words_dataset = open(self.words_path)
        self.dictionary = {}
        self.count = 0
        for word in self.words_dataset:
            # dictionary['你好']=50，当我们遇到'你好'的时候，就将向量的第50位变为1
            self.dictionary[word.replace('\n','')] = self.count # 去掉字体后面的\n转折
            self.count += 1
        '''
        2，读取积极和消极词汇，进行分词
        '''
        x = []
        y = []
        raw_data = []
        positive_txt = open(positive_path)
        negative_txt = open(negative_path)

        #读取积极数据
        for sentence in positive_txt:
            # 创建一个全为0的向量。[0，0，0，0...0，0，0]
            x_vec = np.zeros(self.count+1)                    #设置初始化向量
            # 对sentence进行分词
            after_split = " ".join(jieba.cut(sentence))  #分词
            words = after_split.split(" ")
            for i in words:
                # 删除分词后的无用字符
                i = i.replace('\n','')
                i = i.replace('\r','')
                i = i.replace(' ','')

                #找到单词所对应向量的下标，并将其变为1
                if self.dictionary.__contains__(i.encode('utf-8')):
                    x_vec[self.dictionary[i.encode('utf-8')]] = 1.
                    # print i + " : "+ str(dictionary[i.encode('utf-8')])
                # else:
                #     print 'Cannot find: '+i
            raw_data.append([x_vec, 1.])

        #读取消极数据
        for sentence in negative_txt:
            x_vec = np.zeros(self.count+1)                    #设置初始化向量
            after_split = " ".join(jieba.cut(sentence))  #分词
            words = after_split.split(" ")
            for i in words:
                i = i.replace('\n','')
                i = i.replace('\r','')
                i = i.replace(' ','')
                if self.dictionary.__contains__(i.encode('utf-8')):

                    x_vec[self.dictionary[i.encode('utf-8')]] = 1.
                    # print i + " : "+ str(dictionary[i.encode('utf-8')])
                # else:
                #     print 'Cannot find: '+i
            raw_data.append([x_vec, 0.])

        #shuffle数据，以便训练
        random.shuffle(raw_data)
        # print raw_data
        for i in raw_data:
            x.append(i[0])
            y.append(i[1])

        '''
        3,对SVM进行训练
        '''
        # mySVM = svm.SVC(kernel='rbf')
        self.mySVM = svm.SVC()
        self.mySVM.fit(x,y)


    def test(self, input_str):
        '''
        4，进行测试：输入一个中文字符串，用SVM判断其是正向情感还是负向情感
        '''
        test_input = input_str
        x_test = np.zeros(self.count+1)                    #设置初始化向量
        after_split = " ".join(jieba.cut(test_input))  #分词
        words = after_split.split(" ")
        for i in words:
            i = i.replace('\n','')
            i = i.replace('\r','')
            i = i.replace(' ','')
            if self.dictionary.__contains__(i.encode('utf-8')):
                x_test[self.dictionary[i.encode('utf-8')]] = 1.
            # else:
            #     print 'Cannot find: '+i

		#负向为0，正向为1
        if self.mySVM.predict([x_test]) == 1.:
            return 1
        else:
            return 0