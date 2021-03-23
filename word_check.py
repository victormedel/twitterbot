import enchant


def word_check(trending_words):
    d = enchant.Dict("en_US")
    
    for word in trending_words:
        if not d.check(word):
            trending_words.remove(word)

    return trending_words