import os
import re
import simplejson as json

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_login import login_required, logout_user, current_user, login_user, LoginManager
from flask_session import Session
from sqlalchemy import create_engine, and_, or_, func
from sqlalchemy.orm import scoped_session, sessionmaker
from models import *
   
app = Flask(__name__)
app.secret_key = 'Z5j2Ed6GLiwvL4N72pl1YRWn80Kq2MLhxWcC1KziFdg'

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    else:
        return render_template("index.html")

@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    res = ''
    isbn = ''
    title = ''
    author = ''
    msg = ''
    if request.method == 'POST':
        # Create variables for easy access
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        
        conditions = []
        if isbn:
            conditions.append(Book.isbn.like("%"+isbn+"%"))
        if title:
            conditions.append(Book.title.ilike("%"+title+"%"))
        if author:
            conditions.append(Book.author.ilike("%"+author+"%"))

        books = Book.query.filter(and_(*conditions)).all();
        # If account exists show error and validation checks
        if len(books) != 0:
            res = books
        else:
            msg = 'No result found'
    return render_template("search.html", res=res, isbn=isbn, title=title, author=author, msg=msg)

@app.route("/book/<int:book_id>", methods=['GET', 'POST'])
@login_required
def book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return ""
    
    msg = '';
    user_id = current_user.get_id()
     # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'rating' in request.form and 'review_text' in request.form:
        # Create variables for easy access
        rating = request.form['rating']
        review_text = request.form['review_text']
        if rating == "":
            msg = "Select Rating. "
        if review_text == "":
            msg = msg + "Enter Review text."
        else:
            review = Review(rating=rating, review_text=review_text, book_id=book.id, user_id=user_id)
            db.session.add(review)
            db.session.commit()
            msg = 'You have successfully submitted review!'
            return redirect(url_for('book',book_id=book.id))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    
    #goodreads result
    import requests
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "GOGXxATEnXyDezVlnmy6Dg", "isbns": book.isbn})
    gr_reviews_count = ''
    gr_rating = ''
    if res:
        json_res = json.loads(res.text)
        gr_reviews_count=json_res['books'][0]['work_reviews_count']
        gr_rating=json_res['books'][0]['average_rating']
    # get all reviews
    review = Review.query.filter(and_(Review.book_id==book_id, Review.user_id==user_id)).first()

    return render_template("book.html", review=review, book=book, gr_reviews_count=gr_reviews_count, gr_rating=gr_rating, msg=msg)

@app.route("/api/<string:isbn>")
def api(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    
    if book:
        review_count = Review.query.filter_by(book_id=book.id).count()
        average_score = Review.query.with_entities(func.avg(Review.rating).label("avarage")).filter_by(book_id=book.id).scalar()
        return jsonify(
            title=book.title,
            author=book.author,
            year=book.author,
            isbn=book.isbn,
            review_count=review_count,
            average_score=round(average_score,2)
        )
    else:
        return "No data found"
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(and_(User.username == username, User.password == password)).first()
        # If account exists show error and validation checks
        if user is None:
            msg = 'Invalid Username or password'
        else:
            #print(user)
            login_user(user)
            msg = 'logged in'
            return redirect(url_for('search'))
    return render_template('index.html', msg=msg)


@app.route('/login/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('search'))
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if account exists using MySQL
        user_count = User.query.filter_by(username=username).count()
        # If account exists show error and validation checks
        if user_count > 0:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            newuser = User(username=username, password=password, email=email)
            db.session.add(newuser)
            db.session.commit()
            msg = 'You have successfully registered!'
            
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)
