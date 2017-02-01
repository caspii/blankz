from google.appengine.ext import ndb

class Game(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False)
    slots = ndb.IntegerProperty(default=5)

    def create_slots(self):
        "Creates all slots required for the game in the Datastore"
        slot_list = []
        for counter in range(0,self.slots):
            slot_list.append(Slot(game=self.key, slot_order=counter))
        ndb.put_multi(slot_list) # Batch datastore operation


class Slot(ndb.Model):
    game = ndb.KeyProperty(Game)
    slot_order = ndb.IntegerProperty()
    text = ndb.StringProperty()
    reserved = ndb.BooleanProperty(default=False)
