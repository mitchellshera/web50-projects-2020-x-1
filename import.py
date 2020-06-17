import os

from flask import Flask
from models import *
import csv

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

def main():
    b = open("books.csv")
    reader = csv.reader(b)
    #Skip header
    headers = next(reader)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()