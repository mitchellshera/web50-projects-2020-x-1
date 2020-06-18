# web50-projects-2020-x-1

# Project 1 - Books (Python, Flask, SQL)

In this project, you’ll build a book review website. Users will be able to register for your website and then log in using their username and password. Once they log in, they will be able to search for books, leave reviews for individual books, and see the reviews made by other people. You’ll also use the a third-party API by Goodreads, another book review website, to pull in ratings from a broader audience. Finally, users will be able to query for book details and book reviews programmatically via your website’s API.

Start Up commands
-----------------


    $ pip3 install -r requirements.txt


    $ set FLASK_APP=application.py
	

    $ set DATABASE_URL=<DATABASE_URL>

    $ flask run
	
Usage
-----

    >>> import requests
    >>> res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "KEY", "isbns": "9781632168146"})
    >>> res.json()
    {'books': [{
                'id': 29207858,
                'isbn': '1632168146',
                'isbn13': '9781632168146',
                'ratings_count': 0,
                'reviews_count': 1,
                'text_reviews_count': 0,
                'work_ratings_count': 26,
                'work_reviews_count': 113,
                'work_text_reviews_count': 10,
                'average_rating': '4.04'
            }]
	}

To import Books data


    $ python3 import.py
	
Resources
---------

* `Goodreads API Docs`_

Goodreads API Docs: https://www.goodreads.com/api/index
Navigate to https://www.goodreads.com/api/keys and apply for an API key

Rationale
---------

There are a number of Goodreads API wrapper libraries out there, but most are
either abandoned or the code is some combination of odd, undocumented,
untested, or incomplete in its API coverage.


## Features

### User Registration
User registration is required in order to use web features.
![register](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/register.PNG)

### Login
Registerd user can login to web.
![login](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/login.PNG)

### Search
Users can search for book by ISBN, Book Title or Book Author.
![search](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/search.PNG)


### Search Result
Search Result shows result based on search criteria (ISBN, Title, Author, Year)
![search_result](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/search_result.PNG)



### Book Details
Details page shows User Review Details (if already submitted by user), Goodreads Review Details section.
Details page allows user to submit review only once. 
![book_details](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/book_details.PNG)
![book_details_user_review](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/book_details_user_review.PNG)


### API Access
If users make a GET request to your website’s /api/<isbn> It returns resulting JSON
![api_valid](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/api_valid.PNG)
![api_invalid](https://raw.githubusercontent.com/vaishalijagtap/web50-projects-2020-x-1/master/screens/api_invalid.PNG)

### Screencast presentation [here](https://youtu.be/_htSZMUoHyw)
