from flask import request, session, render_template
# from app import app, db
from models import Category, Article, User


@app.route('/category/create', methods=['GET', 'POST'])
def category_create():
    if request.method == 'POST':
        pass
