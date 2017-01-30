from google.appengine.ext import ndb

class Game(ndb.Model):
    name = ndb.StringProperty()
    blank1 = ndb.StringProperty()
    blank2 = ndb.StringProperty()
