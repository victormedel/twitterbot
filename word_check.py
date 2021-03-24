from english_words import english_words_set

def word_check(trending_words):
    
    for word in trending_words:
        if word not in english_words_set:
            trending_words.remove(word)

    return trending_words