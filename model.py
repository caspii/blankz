from google.appengine.ext import ndb
from flask import session

class SlotState:
    Free, Reserved, Complete = range(3)

class Game(ndb.Model):
    date_created =  ndb.DateTimeProperty(auto_now=True)
    date_altered =  ndb.DateTimeProperty(auto_now_add=True)
    slot_count =    ndb.IntegerProperty(default=6)
    game_type =     ndb.IntegerProperty(default=1)
    emails =        ndb.StringProperty()

    @classmethod
    def new(cls):
        new_game = Game()
        new_game_key = new_game.put()
        slot_list = []
        for counter in range(0, new_game.slot_count):
            slot_list.append(Slot(parent=new_game_key, slot_order=counter))
        ndb.put_multi(slot_list) # Batch datastore operation
        return new_game

    @classmethod
    def get_game(cls, game_key):
        game_key = ndb.Key(urlsafe=game_key)
        return game_key.get()

    def get_game_key(self):
        return self.key.urlsafe()

    def get_completed_slots(self):
        slots_query = Slot.query(Slot.state == SlotState.Complete, ancestor=self.key).order(Slot.slot_order)
        slots = []
        for slot in slots_query:
            slots.append(slot)
        return slots

    def get_free_slot(self):
        """
        Returns one free slot, unreserved if possible, and reserves it.

        Slot is saved in session so that user cannot accidentally reserve
        multiple slots (by reloading page)
        """
        session_slot_key = 'slot' + str(self.key.id())
        if session.get(session_slot_key) is None:
            # No reserved slot is stored in the session
            slots_query = Slot.query(Slot.state < SlotState.Complete, ancestor=self.key)
            slots_query.order(Slot.state) # sort unreserved slots to top
            free_slot = slots_query.get()
            # reserve slot
            if free_slot is not None:
                session[session_slot_key] = free_slot.key.urlsafe()
                if free_slot.state < SlotState.Complete:
                    free_slot.state = SlotState.Reserved
                    free_slot.put()

        else:
            slot_url = session.get(session_slot_key)
            free_slot = ndb.Key(urlsafe=slot_url).get()
            free_slot.state = SlotState.Reserved # make it possible to edit own old slot
            free_slot.put()
        return free_slot

    def save_email(self, email):
        """Write the given email into the repeated property. Duplicates are not saved"""
        if self.emails is not None:
            emails_list = self.emails.split(',')
        else:
            emails_list = []
        emails_list.append(email)
        self.emails = ','.join(set(emails_list))
        self.put()


class Slot(ndb.Model):
    """
    """
    date_altered = ndb.DateTimeProperty(auto_now_add=True)
    slot_order = ndb.IntegerProperty()
    text = ndb.StringProperty()
    state = ndb.IntegerProperty(default=SlotState.Free)

    @classmethod
    def get_slot(cls, game_key):
        slot_key = ndb.Key(urlsafe=game_key)
        return slot_key.get()

    def get_slot_key(self):
        return self.key.urlsafe()

    def save(self, text):
        self.text = text
        self.state = SlotState.Complete
        self.put()
