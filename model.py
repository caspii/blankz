from google.appengine.ext import ndb

class Game(ndb.Model):
    date_created = ndb.DateTimeProperty(auto_now=True)
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    complete = ndb.BooleanProperty(default=False)
    slot_count = ndb.IntegerProperty(default=5)

    @classmethod
    def new(cls):
        new_game = Game()
        new_game_key = new_game.put()
        slot_list = []
        for counter in range(0, new_game.slot_count):
            slot_list.append(Slot(parent=new_game_key, slot_order=counter))
        ndb.put_multi(slot_list) # Batch datastore operation
        print "Created slots"
        return new_game

    @classmethod
    def get_game(cls, url_string):
        game_key = ndb.Key(urlsafe=url_string)
        game = game_key.get()
        return game

    def get_url_string(self):
        return self.key.urlsafe()

    def get_completed_slots(self):
        slots_query = Slot.query(Slot.state == 3, ancestor=self.key)
        slots = []
        for slot in slots_query:
            slots.append(slot)
        return slots

    def get_incomplete_slot(self):
        """
        Returns one slot, unreserved if possible, and reserves it
        """
        slots_query = Slot.query(Slot.state < 3, ancestor=self.key)
        slots_query.order(Slot.state) # sort unreserved slots to top
        incomplete_slot = slots_query.get()
        print "Got incomplete slot: " + str(incomplete_slot)
        # reserve slot
        if incomplete_slot is not None:
            incomplete_slot.state = 1
            incomplete_slot.put()
        return incomplete_slot


class Slot(ndb.Model):
    """
    state 0 = slot free
    state 1 = slot reserved
    state 3 = slot completed
    """
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    slot_order = ndb.IntegerProperty()
    text = ndb.StringProperty()
    state = ndb.IntegerProperty(default=0)

    def save(self, text):
        self.text = text
        self.state = 3
        self.put()
