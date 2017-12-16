#encoding: utf-8
from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Question,Answer
from exts import db
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('create_time').all()
    }
    return render_template('index.html', **context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 31天内都不需要再登录
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u"手机号或密码错误，请重新输入"


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # 手机号码验证
        user = User.query.filter(User.telephone == telephone).first()
        if(user):
            return u"该手机号码已经注册，请更换手机号码！"
        else:
            # 两次输入的mm相等才可以
            if password1 != password2:
                return u"两次密码不相等，请重新输入"
            else:
                user = User(telephone=telephone,username=username,password = password1)
                db.session.add(user)
                db.session.commit()

                # 注册成功，跳转到登陆页面
                return redirect(url_for('login'))

@app.route("/logout/")
def logout():
    # session.pop("user_id")
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))

@app.route("/question/",methods=['GET','POST'])
#@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('user_id')
        user = User.query.filter(User.id==user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=question_model)

@app.route('/add_answer/',methods=["POST"])
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content = content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    answer.author = user
    question =  Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    # title ,content
    questions = Question.query.filter(or_(Question.title.contains(q),
                                          Question.content.contains(q))).order_by('create_time')
    return render_template('index.html',questions = questions)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user':user}
    return{}

if __name__ == '__main__':
    app.run()
