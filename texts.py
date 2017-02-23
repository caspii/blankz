
texts = [
    # Slot 1
    (
        ("Give a name for the man in the story", "Example: Pete, or Richard the Lionheart"),
        ("Enter what the woman in the story said", "Example: I wish I was little bit taller")
    ),
    # Slot 2
    (
        ("Give a name for the woman in the story", "Example: Delilah, or Miss Moneypenny"),
        ("Enter what the man in the story said", "Example: I wish I was little bit taller")
    ),
    # Slot 3
    (
        ("Give an adjective describing the woman", "Example: Very tall, or sleepy, or embarrassed"),
        ("Enter what the man is wearing", "Example: a a pink tutu or a suit-of-armour")
    ),
    # Slot 4
    (
        ("Give an adjective describing the man", "Example: Very tall, or sleepy, or embarrassed"),
        ("Enter what the woman is wearing", "Example: a pink tutu or a suit-of-armour")    ),
    # Slot 5
    (
        ("Give a location where the story takes place", "Example: in a graveyard, or Hogwarts"),
        ("Enter what the consequence was", "Example: they drove off into the sunset together")
    ),

]

def get_texts_for_slot(slot_order):
    """
    Return descriptive texts and placeholders for the given slot.
    """
    return texts[slot_order]
