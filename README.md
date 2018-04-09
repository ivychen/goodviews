# GoodViews

A cinema database and discussion platform.

## Project 1 Part 3

TODO:
A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway. If you did not implement some part of the proposal in Part 1, explain why.
Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.

1. The PostgreSQL account where DB resides: ic2389
2. URL of web application: [http://35.185.29.235:8111](http://35.185.29.235:8111)
3. Features implemented:
    - User login/registration


03-01-2018:

- Updated SQL after Kim's feedback
- Added `NOT NULL` and `CHECK` constraints
- Replaced all instances of `CHAR` iwth `VARCHAR`
- Converted unique identifiers (<id>) to `SERIAL` type, foreign keys still `INTEGER`



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
```

---

COMS4111 Database Systems

Team: Ivy Chen & Gregory Yap
