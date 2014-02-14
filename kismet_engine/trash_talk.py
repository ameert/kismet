import random
phrases = ['Wow...great choice?',
           'Hmmm...you might be getting better',
           'Not bad plying for a human',
           "I'm getting worried that I won't double your score",
           "That's not even worth a comment"]


def trash_talk():
    """returns a random trash talk phrase from the list of phrases"""
    return random.choice(phrases)


