"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver
To run locally:
    python server.py
Go to http://localhost:8111 in your browser.
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""
import os
from datetime import datetime
  # accessible as a variable in index.html:
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, url_for, request, render_template, g, redirect, Response
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

# Import custom modules
from user_class import User


# Create app
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# Enable flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of:
#
#     postgresql://USER:PASSWORD@35.227.79.146/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.227.79.146/proj1part2"
#
DATABASEURI = "postgresql://ic2389:goodviews@35.227.79.146/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
    """
    This function is run at the beginning of every web request
    (every time you enter an address in the web browser).
    We use it to setup a database connection that can be used throughout the request.

    The variable g is globally accessible.
    """
    try:
        g.conn = engine.connect()
    except:
        print("uh oh, problem connecting to database")
        import traceback; traceback.print_exc()
        g.conn = None

@app.teardown_request
def teardown_request(exception):
    """
    At the end of the web request, this makes sure to close the database connection.
    If you don't, the database could run out of memory!
    """
    try:
        g.conn.close()
    except Exception as e:
        pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
#
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
    """
    request is a special object that Flask provides to access web request information:

    request.method:   "GET" or "POST"
    request.form:     if the browser submitted a form, this contains the data in the form
    request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

    See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
    """

    # DEBUG: this is debugging code to see what request looks like
    print(request.args)
    print("Index path:", request.path)

    if current_user.is_authenticated:
        return redirect(url_for('main'))

    # render_template looks in the templates/ folder for files.
    # for example, the below file reads template/index.html
    return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
#
#     localhost:8111/main
#
# Notice that the function name is main() rather than index()
# The functions for each app.route need to have different names
@app.route('/main')
@login_required
def main():

    # example of a database query
    # cursor = g.conn.execute("SELECT name FROM test")

    print(current_user)

    # Query: Movies
    cursor = g.conn.execute("SELECT * FROM Movies")
    movies = []
    movies = cursor.fetchall()
    cursor.close()
    # for result in cursor:
    #     rows.append(result)  # can also be accessed using result[0]

    # Query: Talent
    cursor = g.conn.execute("SELECT T.tid, T.name, S.movieID, S.role FROM Talent T, Stars_In S WHERE T.tid = S.tid")
    talent = []
    talent = cursor.fetchall()
    cursor.close()

    # Query Reviews for all
    cursor = g.conn.execute("SELECT M.id, R.rating, R.text, to_char(R.review_date, 'Month DD, YYYY'), U.username FROM Movies M, Review R, Users U WHERE M.id = R.rid AND R.uid = U.uid ORDER BY R.review_date DESC")
    movie_reviews = []
    movie_reviews = cursor.fetchall()
    cursor.close()

    # Query Review aggregate
    cursor = g.conn.execute("SELECT M.id, ROUND(AVG(R.rating),2) FROM Movies M, Review R WHERE M.id = R.rid GROUP BY M.id")
    movie_ratings = []
    movie_ratings = cursor.fetchall()
    cursor.close()

    # Query this user's reviews
    cursor = g.conn.execute("SELECT DISTINCT M.id, R.rating, R.text, to_char(R.review_date, 'Month DD, YYYY') FROM Movies M, Review R, Users U WHERE M.id = R.rid AND R.uid=%s", current_user.uid)
    user_movie_reviews = []
    user_movie_reviews = cursor.fetchall()
    cursor.close()

    # Flask uses Jinja templates, which is an extension to HTML where you can
    # pass data to a template and dynamically generate HTML based on the data
    # (you can think of it as simple PHP)
    # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
    #
    # You can see an example template in templates/index.html
    #
    # context are the variables that are passed to the template.
    # for example, "data" key in the context variable defined below will be
    # accessible as a variable in index.html:
    #
    #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
    #     <div>{{data}}</div>
    #
    #     # creates a <div> tag for each element in data
    #     # will print:
    #     #
    #     #   <div>grace hopper</div>
    #     #   <div>alan turing</div>
    #     #   <div>ada lovelace</div>
    #     #
    #     {% for n in data %}
    #     <div>{{n}}</div>
    #     {% endfor %}
    #
    context = dict(movies=movies, talent=talent, movie_reviews=movie_reviews, movie_ratings=movie_ratings, user_movie_reviews=user_movie_reviews, uid=current_user.uid)

    return render_template("main.html", **context)


@app.route('/write_review', methods=['POST'])
def write_review():
    uid = current_user.uid
    review_date = datetime.now()

    # Upsert bc no PostgreSQL 9.5
    result = g.conn.execute("UPDATE Review SET rating=%s, text=%s, review_date=%s WHERE uid=%s AND rid=%s", request.form['rating'], request.form['text'], review_date, uid, request.form['rid'])

    if result.rowcount == 0:
        g.conn.execute("INSERT INTO Review (rid, uid, rating, text, review_date) VALUES (%s, %s, %s, %s, %s)", request.form['rid'], uid, request.form['rating'], request.form['text'], review_date)

    if "theaters" in request.referrer:
        return redirect('/theaters')
        
    return redirect('/main')


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    print(name)
    g.conn.execute('INSERT INTO test(name) VALUES (%s)', name)
    return redirect('/another')

# === THEATERS ===
@app.route('/theaters')
@login_required
def theaters():
    # Query: Theaters
    cursor = g.conn.execute("SELECT * FROM Theaters T ORDER BY T.name")
    theaters = []
    theaters = cursor.fetchall()
    cursor.close()

    # # Query: Talent
    # cursor = g.conn.execute("SELECT T.tid, T.name, S.movieID, S.role FROM Talent T, Stars_In S WHERE T.tid = S.tid")
    # talent = []
    # talent = cursor.fetchall()
    # cursor.close()

    # Query Reviews for all
    cursor = g.conn.execute("SELECT T.id, R.rating, R.text, to_char(R.review_date, 'Month DD, YYYY'), U.username FROM Theaters T, Review R, Users U WHERE T.id = R.rid AND R.uid = U.uid ORDER BY R.review_date DESC")
    theater_reviews = []
    theater_reviews = cursor.fetchall()
    cursor.close()

    # Query Review aggregate
    cursor = g.conn.execute("SELECT T.id, ROUND(AVG(R.rating),2) FROM Theaters T, Review R WHERE T.id = R.rid GROUP BY T.id")
    theater_ratings = []
    theater_ratings = cursor.fetchall()
    cursor.close()

    # Query this user's reviews for theaters
    cursor = g.conn.execute("SELECT DISTINCT T.id, R.rating, R.text, to_char(R.review_date, 'Month DD, YYYY') FROM Theaters T, Review R, Users U WHERE T.id = R.rid AND R.uid=%s", current_user.uid)
    user_theater_reviews = []
    user_theater_reviews = cursor.fetchall()
    cursor.close()

    # Movie Showings at this Theater
    cursor = g.conn.execute("SELECT M.id, T.id, M.name, M.year, M.genre, M.runtime, M.overview, to_char(S.datetime, 'Month DD, YYYY HH12:MI AM') FROM Theaters T, Movies M, Showing S WHERE T.id = S.theaterID AND M.id = S.movieID ORDER BY M.name ASC")
    movie_showings = []
    movie_showings = cursor.fetchall()
    cursor.close()

    context = dict(theaters=theaters, theater_reviews=theater_reviews, theater_ratings=theater_ratings, user_theater_reviews=user_theater_reviews, movie_showings=movie_showings)

    return render_template("theaters.html", **context)

# === LOGIN ====
@login_manager.user_loader
def load_user(username):
    cursor = g.conn.execute("SELECT * FROM Users U WHERE U.username=%s", username)
    data = cursor.fetchone()
    cursor.close()

    if data is None:
        return None

    return User(data[1], data[2], data[3], data[0])

def authenticate_user(user):
    cursor = g.conn.execute("SELECT * FROM Users U WHERE U.username=%s", user.username)
    data = cursor.fetchone()
    cursor.close()

    if data[2] == user.password:
        return True
    else:
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        test_user = User(request.form['username'], request.form['password'])

        if authenticate_user(test_user):
            login_user(test_user)
            return redirect(url_for('main'))
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    error = None

    if request.method == 'POST':
        try:
            new_user = User(request.form['username'],
                      request.form['password'],
                      request.form['email'])

        except ValueError:
            error = "Username or Password is empty"

        if (not is_registered_user(new_user)):
            register_user(new_user)
            login_user(new_user)
            return redirect(url_for('main'))
        else:
            error = "Username or email taken."

    return render_template('register.html', error=error)

def register_user(user):
    cursor = g.conn.execute("INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)", (user.username, user.password, user.email))

    cursor.close()

def is_registered_user(user):
    cursor = g.conn.execute("SELECT * FROM Users U WHERE U.username=%s", (user.username, ))
    data = cursor.fetchone()
    cursor.close()

    if data:
        return True
    else:
        return False


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


if __name__ == "__main__":
    import click

    @click.command()
    @click.option('--debug', is_flag=True)
    @click.option('--threaded', is_flag=True)
    @click.argument('HOST', default='0.0.0.0')
    @click.argument('PORT', default=8111, type=int)

    def run(debug, threaded, host, port):
        """
        This function handles command line parameters.
        Run the server using:

            python server.py

        Show the help text using:

            python server.py --help

        """

        # App configuration for flask-login
        app.secret_key = 'gravano'

        HOST, PORT = host, port
        print("running on %s:%d" % (HOST, PORT))
        app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)

    run()
