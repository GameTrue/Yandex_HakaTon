from flask import Flask, jsonify, redirect, render_template, session, request, make_response
from flask_restful import reqparse, abort, Api, Resource
from requests import get, post, delete, put
from db import DB, NewsModel, UserModel
from loginform import LoginForm
from registerform import RegisterForm
from settings import SettingsForm
from add_news import AddNewsForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
api = Api(app)

dbase = DB()

parser = reqparse.RequestParser()
parser.add_argument('title', required=False)
parser.add_argument('content', required=False)
parser.add_argument('user_id', required=False, type=int)
parser.add_argument('username', required=False)
parser.add_argument('password', required=False)


@app.errorhandler(404)
def page_not_found(e):
    return redirect('/404')


@app.route('/')
def index():
    return redirect('/news')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', title='Авторизация', form=form, error='')
    elif request.method == 'POST':
        form = LoginForm()
        user_name = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        if user_name == '':
            return render_template('login.html', title='Авторизация', form=form, error='Введите имя пользователя!')
        if password == '':
            return render_template('login.html', title='Авторизация', form=form, error='Введите пароль!')
        if user_name == 'admin' and password == '123':
            session['username'] = 'admin'
            session['admin'] = True
            session['sort'] = 'date'
            session['reverse'] = False
            return redirect('/news')
        user_model = UserModel(dbase.get_connection())
        exists = user_model.exists(user_name, password)
        if not exists[0]:
            return render_template('login.html', title='Авторизация', form=form, error='Неверное имя пользователя или пароль!')
        session['username'] = user_name
        session['user_id'] = exists[1]
        session['remember_me'] = remember_me
        session['sort'] = 'date'
        session['reverse'] = False
        session['admin'] = False
        #print(remember_me)
        return redirect("/news")


@app.route('/logout')
def logout():
    session['username'] = None
    session['user_id'] = None
    session['sort'] = None
    session['reverse'] = None
    session['admin'] = None
    return redirect('/login')

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template('register.html', title='Регистрация', form=form, error='')
    elif request.method == 'POST':
        print('Заходит в пост')
        form = RegisterForm()
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(dbase.get_connection())
        if user_name == '':
            return render_template('register.html', title='Регистрация', form=form, error='Введите имя пользователя!')
        if password == '':
            return render_template('register.html', title='Регистрация', form=form, error='Введите пароль!')
        users = UserModel(dbase.get_connection())
        if not users.insert(user_name, password):
            return render_template('register.html', title='Регистрация', form=form, error='Данный пользователь уже существует!')
        exists = user_model.exists(user_name, password)
        session['username'] = user_name
        session['user_id'] = exists[1]
        session['sort'] = 'date'
        session['reverse'] = False
        session['admin'] = False
        return redirect('/news')
##        if not user_model.insert(user_name, password):
##            return render_template('register.html', title='Регистрация', form=form, error='Данный пользователь уже существует!')
##        exists = user_model.exists(user_name, password)
##        session['username'] = user_name
##        session['user_id'] = exists[1]
##        session['args'] = []
        # photo.save(os.path.dirname(os.path.abspath(__file__)) + '\\static\\' + session['username'] + "\\avatar.png")
        #      os.mkdir('static/' + user_name)
##        return post("/users")

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'admin' in session and session['admin']:
        return redirect('/news')
    if 'user_id' not in session or session['user_id'] == None:
        return redirect('/login')
    if request.method == 'GET':
        form = AddNewsForm()
        return render_template('add_news.html', title='Добавление новости', form=form)
##            if not('username' in session.keys()) or not('remember_me' in session.keys()):
##                return redirect("/login")
##            if not session['remember_me']:
##                session['remember_me'] = None
##            return '''<head>
##                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
##                    
##                </head>
##                <body class="bg-secondary">
##                    
##                </body>
##               
##                    '''
    elif request.method == 'POST':
        form = AddNewsForm()
        news = NewsModel(dbase.get_connection())
        news.insert(form.title.data, form.content.data, session['user_id'])
        return redirect('/news')


@app.route('/delete_news/<int:news_id>')
def delete_news(news_id):
    if not ('admin' in session and session['admin']) and ('user_id' not in session or session['user_id'] == None):
        return redirect('/login')
    abort_if_news_not_found(news_id)
    nm = NewsModel(dbase.get_connection())
    if session['admin'] or nm.get(news_id)[3] == session['user_id']:
        nm.delete(news_id)
    return redirect('/news')


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not ('admin' in session and session['admin']) and ('user_id' not in session or session['user_id'] == None):
        return redirect('/login')
    if request.method == 'GET':
        form = SettingsForm()
        return render_template('settings.html', title='Настройки сортировки', form=form)
    elif request.method == 'POST':
        form = SettingsForm()
        session['reverse'] = form.reverse.data
        session['sort'] = form.sort_type.data
        print(form.reverse.data, form.sort_type.data)
##        news = NewsModel(dbase.get_connection())
##        news.insert(form.title.data, form.content.data, session['user_id'])
        return redirect('/news')

    
@app.route('/404')
def error404():
    return '''
<head>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
</head>
<body>
    <img width="15%" height="40%" class="bige" alt="ERROR" src="static/404.png">
</body>
'''


def abort_if_news_not_found(news_id):
    if not NewsModel(dbase.get_connection()).get(news_id):
        return redirect('/404')


def abort_if_user_not_found(user_id):
    if not UserModel(dbase.get_connection()).get(user_id):
        return redirect('/404')


def check_arg(args, name):
    if name not in args or args[name] is None or str(args[name]) == '':
        return False
    return True


class News(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        news = NewsModel(dbase.get_connection()).get(news_id)
        return make_response('<p><h1>{0}</h1></p><div>{1}</div><p><a href="/news">Вернуться на страницу с новостями</a></p>'.format(news[1], news[2]))
 
    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        NewsModel(dbase.get_connection()).delete(news_id)
        return jsonify({'success': 'OK'})


class NewsList(Resource):
    def get(self):
        if not ('admin' in session and session['admin']) and ('user_id' not in session or session['user_id'] == None):
            return redirect('/login')
##        return redirect('/login')
##        print(NewsModel(dbase.get_connection()).get_all(session['user_id']))
        if session['admin']:
            news = NewsModel(dbase.get_connection()).get_all()
        else:
            news = NewsModel(dbase.get_connection()).get_all(session['user_id'])
        if session['sort'] == 'alphabet':
            news.sort(key=lambda x: x[1] + x[2])
        if session['reverse'] == True:
            news = news[::-1]
        return make_response(render_template('contest.html', title='Главная страница', news=news, admin=session['admin']))
 
    def post(self):
        args = parser.parse_args()
        if check_arg(args, 'title') and check_arg(args, 'content') and check_arg(session, 'user_id'):
            news = NewsModel(dbase.get_connection())
            news.insert(args['title'], args['content'], session['user_id'])
            return redirect('/news')
        return redirect('/login')


##class index(Resource):
##    def get(self):
##        news = NewsModel(dbase.get_connection()).get_all()
##        return jsonify({'news': news})
    

class Users(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        users = UserModel(dbase.get_connection()).get(user_id)
        return jsonify({'users': users})
 
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        UserModel(dbase.get_connection()).delete(user_id)
        return jsonify({'success': 'OK'})

    def put(self, user_id):
        args = parser.parse_args()
        if check_arg(args, 'password'):
            abort_if_user_not_found(user_id)
            UserModel(dbase.get_connection()).change(user_id, 'password_hash', args['password'])
            return jsonify({'success': 'OK'})


class UserList(Resource):
    def get(self):
        if 'admin' not in session or not session['admin']:
            return redirect('/news')
        users = UserModel(dbase.get_connection()).get_all()
        nm = NewsModel(dbase.get_connection())
        users = list(map(lambda x: (x[1], len(nm.get_all(x[0]))), users))
        return make_response(render_template('userlist.html', title='Список пользователей', users=users))
 
    def post(self):
        args = parser.parse_args()
        if check_arg(args, 'username') and check_arg(args, 'password'):
            users = UserModel(dbase.get_connection())
            if not users.insert(args['username'], args['password']):
                return redirect('/register')
            exists = user_model.exists(user_name, password)
            session['username'] = user_name
            session['user_id'] = exists[1]
            session['sort'] = 'date'
            session['reverse'] = False
            return redirect('/news')
        

    
api.add_resource(NewsList, '/news') # для списка объектов
##api.add_resource(index, '/')
api.add_resource(News, '/news/<int:news_id>') # для одного объекта
api.add_resource(Users, '/users/<int:user_id>')
api.add_resource(UserList, '/users')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)
