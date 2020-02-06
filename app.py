from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_migrate import Migrate,MigrateCommand
from order import app_orders
from cart import app_cart


app = Flask(__name__)
# 注册蓝图
# app.register_blueprint(app_orders)
app.register_blueprint(app_orders,url_prefix="/orders")
app.register_blueprint(app_cart, url_prefix="/cart")

class Config(object):
    # 配置参数
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:banGIAN2008@192.168.1.22:3306/test"
    # 设置sqlalchemy自动更新跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = "fasdfasdfoi23423k"


app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager = Manager(app)
# 创建数据库迁移工具对象
Migrate(app, db)
# 向Manager对象中添加数据库的操作命令
manager.add_command("db", MigrateCommand)

class Author(db.Model):
    __tablename__ = "tbl_authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    books = db.relationship("Book", backref="author")


class Book(db.Model):
    __tablename__ = "tbl_books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_authors.id"))

# 创建表单模型类
class AuthorBookForm(FlaskForm):
    # 作者书籍模型类
    author_name = StringField(label="作者",validators=[DataRequired("作者必填")])
    book_name = StringField(label="书籍",validators=[DataRequired("书籍必填")])
    submit = SubmitField(label="保存")

@app.route('/', methods=["get","post"])
def hello_world():
    # 创建表单对象
    form = AuthorBookForm()
    # 只有提交的时候才会执行form.validate_on_submit所以第一次展示的时候不执行
    if form.validate_on_submit():
        # 成功
        author_name = form.author_name.data
        book_name = form.book_name.data
        # 保存数据库
        author = Author(name=author_name)
        db.session.add(author)
        db.session.commit()

        book = Book(name=book_name,author_id=author.id)
        # book = Book(name=book_name, author=author)
        db.session.add(book)
        db.session.commit()

    author_li = Author.query.all()
    return render_template("author_book.html", authors=author_li, form=form)


@app.route("/delete_book", methods=["post"])
def delete_book():
    # 删除数据
    # req_data = request.data
    # json.loads(req_data)
    # 如果前端发送的请求数据是json格式，get_json会解析成字典
    # get_json要求前端传送的数据 也必须是Content-Type:application/json
    req_dict = request.get_json()
    print(req_dict)
    book_id = req_dict.get("book_id")
    # 删除数据
    book = Book.query.get(book_id)
    print(book)
    db.session.delete(book)
    db.session.commit()
    # "Content-Type": "application/json"，前端会自动解析json
    return jsonify(code=0, message="ok")


if __name__ == '__main__':
    print('bbb')
    try:
        print('aaa')
        # app.run()
        # 通过manager启动程序
        manager.run()
        # db.create_all()
        #
        # au_xi = Author(name="我吃西红柿", )
        # au_qian = Author(name="消遣",)
        # au_san = Author(name="唐家三少",)
        # db.session.add_all([au_xi,au_qian,au_san]);
        # db.session.commit()
        #
        # bk_xi = Book(name="吞噬星空", author_id=au_xi.id)
        # bk_xi2 = Book(name="寸芒", author_id=au_qian.id)
        # bk_qian = Book(name="飘渺之旅", author_id=au_san.id)
        # bk_san = Book(name="冰火魔厨", author_id=au_san.id)
        # db.session.add_all([bk_xi,bk_xi2,bk_san,bk_qian])
        # db.session.commit()
    except Exception as e:
        print(e);
    # 通过manager对象