#encoding: utf-8
from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User
from exts import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone,User.password == password).first()
        if user:
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

@app.route("/question/")
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        pass

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
