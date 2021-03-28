#!/usr/bin/env python
# twitter-bot/bot/word_check.py
import enchant

def word_check(trending_words):

    dic = enchant.Dict('en_US') # US English Dictionary
    
    for word in trending_words:
        if not dic.check(word):
            trending_words.remove(word)

    return trending_words
