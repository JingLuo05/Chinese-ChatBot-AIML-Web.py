# -*- coding: utf-8 -*-

import chatting_robot

robot = chatting_robot.ChatRobot()


while 1:
    input = raw_input("请输入：")
    answer = robot.chat(input)
    if answer is "":
        new_answer = raw_input("请输入您的答案：")
        robot.addAnswer(input, new_answer)
    else:
        print answer