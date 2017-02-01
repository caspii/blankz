from google.appengine.ext import ndb

class Game(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False) # new property


class Slot(ndb.Model):
    game = ndb.KeyProperty(Game)
    text = ndb.StringProperty()
    reserved = ndb.BooleanProperty(default=False) # new property
    date_created = ndb.DateTimeProperty(auto_now_add=True)
