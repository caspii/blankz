from google.appengine.ext import ndb

class Game(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now=True)
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False)
    slots = ndb.IntegerProperty(default=5)

    @classmethod
    def new(cls):
        "Creates a game entity, the slots for the game, and returns a url_string"
        new_game = Game()
        new_game_key = new_game.put()
        slot_list = []
        for counter in range(0, new_game.slots):
            slot_list.append(Slot(game=new_game_key, slot_order=counter))
        ndb.put_multi(slot_list) # Batch datastore operation
        return new_game_key.urlsafe()

    @classmethod
    def get_game(cls, url_string):
        game_key = ndb.Key(urlsafe=url_string)
        game = game_key.get()
        slots = Slot.query(ndb.AND(Slot.game == game.key, Slot.state == 3))
        for slot in slots:
            print(slot)
        return game

class Slot(ndb.Model):
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    game = ndb.KeyProperty(Game)
    slot_order = ndb.IntegerProperty()
    text = ndb.StringProperty()
    # state 0 = slot free
    # state 1 = slot reserved
    # state 3 = slot completed
    state = ndb.IntegerProperty(default=0)
