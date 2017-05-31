# -*- coding: utf-8 -*-

stop_words_path = "./res/stop_words.txt"

def eliminate_stop_words(sentence):
    stop_words = []
    file_input = open(stop_words_path)
    for i in file_input:
        stop_words.append(i.replace('\n',''))
    result = sentence
    for i in stop_words:
        result = result.replace(i,'')
    return result

