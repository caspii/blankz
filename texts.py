
texts = [
    # Slot 1
    (
        ("Give a name for the man in the story", "for example: Pete, or Richard the Lionheart"),
        ("Enter what the woman in the story said", "for example: I wish I was little bit taller")
    ),
    # Slot 2
    (
        ("Give a name for the woman in the story", "for example: Delilah, or Miss Moneypenny"),
        ("Enter what the man in the story said", "for example: I wish I was little bit taller")
    ),
    # Slot 3
    (
        ("Give an adjective describing the woman", "for example: Very tall, or sleepy, or embarrassed"),
        ("Enter what the man is wearing", "for example: a a pink tutu or a suit-of-armour")
    ),
    # Slot 4
    (
        ("Give an adjective describing the man", "for example: Very tall, or sleepy, or embarrassed"),
        ("Enter what the woman is wearing", "for example: a pink tutu or a suit-of-armour")    ),
    # Slot 5
    (
        ("Give a location where the story takes place", "for example: in a graveyard, or at Buckingham Palace"),
        ("Enter what the consequence was", "for example: they drove off into the sunset together")
    ),

]

def get_texts_for_slot(slot_order):
    """
    Return descriptive texts and placeholders for the given slot.
    """
    print slot_order
    return texts[slot_order]
