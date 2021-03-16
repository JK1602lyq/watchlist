import os
import sys
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import click

app = Flask(__name__)


WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统， 使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'
# app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
db = SQLAlchemy(app)


@app.cli.command() # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')
# 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息


class User(db.Model):  # 表名将会是 user（ 自动生成， 小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
    db.session.add(movie)
    db.session.commit()
    click.echo('Done.')


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)

# @app.route('/')
# def hello():
#     return 'Hello'
# @app.route('/user/<name>')
# def user_page(name):
#     return 'User: %s' % name
# @app.route('/test')
# def test_url_for():
# # 下面是一些调用示例（ 请在命令行窗口查看输出的 URL） ：
#     print(url_for('hello')) # 输出： /
# # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
#     print(url_for('user_page', name='greyli')) # 输出： /user/greyli
#     print(url_for('user_page', name='peter')) # 输出： /user/peter
#     print(url_for('test_url_for')) # 输出： /test
# # 下面这个调用传入了多余的关键字参数， 它们会被作为查询字符串附加到 URL后面。
#     print(url_for('test_url_for', num=2)) # 输出： /test?num=2
#     return 'Test page'

# app = Flask(__name__)
# @app.route('/')
# @app.route('/home')
# @app.route('/index')
# @app.route('/login/<name>')
# def hello(name):
#    return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'+'<h1>User: %s<h1>' % name
