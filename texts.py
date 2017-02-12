
texts = [
    ("Enter a man's name", "for example: Pete, or Richard the Lionheart"),
    ("Enter a woman's name", "for example: Delilah, or Miss Moneypenny"),
    ("Enter a place or location", "for example: at the dentists"),
    ("Enter what the man said", "for example: you sure smell bad today"),
    ("Enter what the woman said", "for example: I wish I was little bit taller"),
    ("Enter what the consequence was", "for example: they drove off into the sunset together"),
]


def get_text_for_slot(slot_order):
    """
    Returns descriptive text for the given slot.
        game_type will in future be used to allow different games
    """
    return texts[slot_order]
