from google.appengine.ext import ndb

class Game(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now=True)
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False)
    slots = ndb.IntegerProperty(default=5)

    def create_slots(self, game_key):
        "Creates all slots required for the game in the Datastore"
        slot_list = []
        print self
        for counter in range(0,self.slots):
            #slot_list.append(Slot(game=self.key, slot_order=counter))
            Slot(game=game_key, slot_order=counter).put()
        #ndb.put_multi(slot_list) # Batch datastore operation


class Slot(ndb.Model):
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    game = ndb.KeyProperty(Game)
    slot_order = ndb.IntegerProperty()
    text = ndb.StringProperty()
    # state 0 = slot free
    # state 1 = slot reserved
    # state 3 = slot completed
    state = ndb.IntegerProperty(default=0)
