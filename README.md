# GoodViews

A cinema database and discussion platform.

COMS4111 Introduction to Database Systems

Prof. Luis Gravano

TA Mentor: Kim Tao

Team: Ivy Chen & Gregory Yap

---

## Project 1 Part 3

**NOTE: Implementation in Python 3.5**

**Proposal Description:** Goodviews is a platform for cinema/theater information and ticket reservation. While sites such as IMDB and RottenTomatoes exist to provide audiences with the latest film, TV and celebrity content and allow users to post reviews of media content, they lack a sense of social community. Furthermore, existing platforms often lack coherence due to the variety of media content. In Goodviews, we aim to marry the best aspects of Goodreads and IMDB and create a digital community of film fans. We offer a more ​streamlined ​database by focusing on movies rather than TV shows or other media. Users can curate ​collections ​of movies (such as "Movies I Want To Watch"), browse actors and post ​reviews ​of movies. They will be able to search a ​robust database ​ for films based on year/genre/rating, browse
plot synopsis, and post reviews on movies or theaters.

We satisfied the following 3 requirements. Functionality is detailed in the sections below:

1. Your application must execute SQL query strings on your database on our class's PostgreSQL server. You cannot use an Object-Relational Mapper, or ORM. An important goal of this project is that you practice writing and debugging SQL queries as part of your application, so tools that attempt to make this "too easy" are not permitted.
2. Your application must provide a way to view or interact with all the entities and relationships in your final E/R diagram.
Your application's web interface does not need to be beautiful or sophisticated. Plain text pages are acceptable. You will not get additional credit for fancy interfaces, as this is not the focus of our course.
3. In general, you can use any third-party libraries you want except for ORMs or other libraries that simplify database access, which are not allowed. If you are unsure if a library is permitted, ask your project mentor.

**Front-End:** We use the Materialize framework (essentially a substitute for Boostrap) for the front-end. It only handles UI interactions and doesn't perform any data handling/processing. The only JavaScript we write is calls to UI component initializers (eg. that handle things like automatically hiding side navigation and opening on button click). See `static/js/main.js` file for more information.

1. The PostgreSQL account where DB resides: ic2389
2. URL of web application: [http://35.185.29.235:8111](http://35.185.29.235:8111)
3. Features Implemented:
    - User:
        - User may login/register for an account
        - Users REVIEW Reviewable (Movies, Theaters)
    - Movies:
        - Browse movie database on main page and easily view details on plot synopsis
        - View Talent that STARS_IN Movies
        - Movies ISA Reviewable, you can view reviews of movies
        - Users can post/update REVIEW of Movies
				- Users can search for Movies by name, year or genre
    - Talent:
        - View Talent that STARS_IN Movies
    - Theaters:
        - Theaters ISA Reviewable, you can view reviews of theaters
        - Theaters SHOW Movies at TimeSlots
        - Users can browse the selection of Showings of Movies for each Theater
    - Collections:
        - Users can view their Collections on the My Collections page
        - Collections CONTAIN Movies
        - Allow users to create Collections on the Collections page
        - Users can add to existing Collections on the Movies page
    - Book:
        - Users can view their Bookings
        - Users BOOK (SHOWINGS of Movies in Theaters during TimeSlots)
4. Features Not Implemented:
    - NA
5. Two web pages that require the most interesting database queries:
    - `/main` page shows Movies in the database, allows User to browse movies and information such as year, genre, runtime and overview. It shows the Talent that stars in a given movie and Reviews for each movie. On this page, we allow users to write reviews by inputing a rating and review text, which INSERTs a review tuple (or UPDATE it if a review for a movie by the current user already exists). In addition, if a user's review already exists for the movie, the form actually shows the previous review. This page is interesting because it shows a lot of information on movies, stars in each movie, and offers functionality for both browsing other users' reviews and writing reviews. Users are also able to search for movies by name, year or genre.
    - `/theaters` page shows Theaters in the database, displays information such as address, contact info and seat capacity. It shows the Showings at each Theater and allows Users to Book tickets using a form that INSERTs a Book tuple (if it exists, UPDATE the booking). In addition, the page shows the User's existing ticket Bookings. We also display the Reviews for each Theater and allow the User to write a review for each Theater (which inserts a rating and review text, or updates the existing review if it already exists). This page is interesting becuase it offers information on theaters, movie showings at each theater, reviews for theaters, the user's movie showing bookings, and offers functionality for booking showings and writing reviews on the same page.

---

## Developer Walkthrough

### Set up Python 3 environment

```py
# Install python 3 dependencies and virtualenv

sudo apt-get install postgresql-9.3 postgresql-server-dev-9.3 git python3-dev python3-pip
sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
virtualenv -p python3 env
source env/bin/activate

# Navigate to goodviews directory and install modules

cd goodviews
pip install -r requirements.txt

# Start server on IPADDRESS:8111, navigate on browser
python server-python3.py
```

---

## Project Feedback/Changelog

03-01-2018:

- Updated SQL after Kim's feedback
- Added `NOT NULL` and `CHECK` constraints
- Replaced all instances of `CHAR` iwth `VARCHAR`
- Converted unique identifiers (<id>) to `SERIAL` type, foreign keys still `INTEGER`
