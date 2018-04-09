import main
import datetime

class User():
  def __init__(self , username, password , email=None):
    if username == "":
      raise ValueError("Username cannot be empty")

    if password == "":
      raise ValueError("Password cannot be empty")

    self.username = username
    self.password = password
    self.email = email
 
  def is_authenticated(self):
    return True
 
  def is_active(self):
    return True
 
  def is_anonymous(self):
    return False
 
  def get_id(self):
    return unicode(self.id)

  def __repr__(self):
    return '<User %r>' % (self.username)

  def __eq__(self, other):
    if self.username == other.username and self.password == other.password:
      return True
    else:
      return False
