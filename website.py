# -*- coding: utf-8 -*-
import web
from web import form
import chatting_robot
import stopwords

#=============chatting robot======
robot = chatting_robot.ChatRobot()

# ============network ========
'''
-->see :  http://webpy.org/docs/0.3/tutorial
web.py:
    目录结构：
        |--Templates
        |--Python

'''

# 将默认的templates目录设置为'templates／'
render = web.template.render('templates/')


# ／ 对应的是index类
urls = (
    '/', 'index',
    '/answer', 'answer',
    '/add','add'
)
app = web.application(urls, globals())

myform = form.Form(
    form.Textbox('输入',id="question",autofocus="autofocus"),
    )

formA = form.Form(
    form.Textbox('Answer',autofocus="autofocus"),
    )

answer = ""
question = ""
after_question = ""
chat_history = [""]


class index:
    def GET(self):
        form = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        global chat_history
        chat_history = []

        return render.formtest(form)

    def POST(self):
        form = myform()
        if not form.validates():
            return render.formtest(form)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            global question
            global answer
            global chat_history
            global after_question
            question = form['输入'].value
            after_question = stopwords.eliminate_stop_words(question)
            answer = robot.chat(after_question)
            chat_history.append(question)
            chat_history.append(answer)

            if answer is "":
                raise web.seeother('/add')
            web.header('Content-Type','text/html; charset=utf-8', unique=True)  # let the browser use the utf-8 encoding
            form['输入'].set_value('')
            return render.answer(answer,chat_history, form)
            # return "Grrreat success! boe: %s, bax: %s, area: %s" % (form.d.boe, form['bax'].value, form['moe'].value)

class answer:

    def GET(self):
        return render.formtest(form)

    def POST(self):
        raise web.seeother('/')


class add:

    new_question = ""

    def GET(self):
        form = formA()
        self.new_question = question
        return render.add(question, form)

    def POST(self):
        form = formA()
        self.new_question = question
        if not form.validates():
            return render.add(question, form)
        else:
            new_answer = form['Answer'].value
            web.header('Content-Type','text/html; charset=utf-8', unique=True)
            print self.new_question
            global after_question
            robot.addAnswer(after_question, new_answer)
            raise web.seeother('/')



if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()



