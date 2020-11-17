from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, session, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/myblog'
app.config[' SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    articles = db.relationship('Article', backref="user_articles", lazy="dynamic")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    articles = db.relationship('Article', backref="cate_articles", lazy="dynamic")


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    views = db.Integer()
    body = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)
    updated_time = db.Column(db.DateTime, default=datetime.now)


# 分类接口
@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = Category(name=name, description=description)
        db.session.add(category)
        try:
            db.session.commit()
        except Exception as ex:
            return '创建失败'
        else:
            return '创建成功', 201
    return render_template('category_create.html')


@app.route('/category/delete/<id>')
def category_delete(id):
    category = Category.query.get(id)
    if not category:
        return '所删除Category不存在'
    db.session.delete(category)
    db.session.commit()
    return '删除成功', 204


@app.route('/category/update/<id>', methods=['GET', 'POST'])
def category_update(id):
    category = Category.query.get(id)
    if not category:
        return '所修改Category不存在'
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        if name:
            category.name = name
        if description:
            category.description = description
        db.session.commit()
        return '修改成功'
    return render_template('category_update.html', category=category)


@app.route('/category/list')
def category_list():
    categories = Category.query.all()
    return render_template('category_list.html', categories=categories)


@app.route('/category/detail/<id>')
def category_detail(id):
    category = Category.query.get(id)
    if not category:
        return '所查询Category不存在'
    return render_template('category_detail.html', category=category)


# 文章接口
@app.route('/article/create', methods=['GET', 'POST'])
def article_create():
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        author_id = request.form.get('author_id')
        title = request.form.get('title')
        views = 0
        body = request.form.get('body')
        article = Article(category_id=category_id, author_id=author_id, title=title, views=views, body=body)
        db.session.add(article)
        try:
            db.session.commit()
        except Exception as ex:
            return '创建失败'
        else:
            return '创建成功', 201
    return render_template('article_create.html')


@app.route('/article/delete/<id>')
def article_delete(id):
    article = Article.query.get(id)
    if not article:
        return '所删除Article不存在'
    db.session.delete(article)
    db.session.commit()
    return '删除成功', 204


@app.route('/article/update/<id>', methods=['GET', 'POST'])
def article_update(id):
    article = Article.query.get(id)
    if not article:
        return '所修改Article不存在'
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        title = request.form.get('title')
        body = request.form.get('body')
        if category_id:
            article.category_id = category_id
        if title:
            article.title = title
        if body:
            article.body = body
        db.session.commit()
        return '修改成功'
    return render_template('article_update.html', article=article)


@app.route('/article/list')
def article_list():
    articles = Article.query.all()
    return render_template('article_list.html', articles=articles)


@app.route('/article/detail/<id>')
def article_detail(id):
    article = Article.query.get(id)
    if not article:
        return '所查询Article不存在'
    return render_template('article_detail.html', article=article)


@app.route('/')
def index():
    categories = Category.query.all()

    articles = Article.query.all()
    return render_template('index.html', articles=articles, categories=categories)


if __name__ == "__main__":
    app.run()
    # db.create_all()
