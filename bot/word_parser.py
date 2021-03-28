#!/usr/bin/env python
# twitter-bot/bot/word_parser.py
import os
import re

def upper_check(value):
    # Counts the number of uppercase letters
    count=0
    for i in value:
        if i.isupper():
            count=count+1

    # Seperate long string that is composed with multiple uppercase and lowercase letters
    if count < len(value):
        result_values = []
        result_values = re.findall('[A-Z][^A-Z]*', value)
        return result_values
    else:
        return value


def double_check(words):
    for word in words:
        if '.' in word:
            new_word = word.replace('.', '')
            words.remove(word)
            words.append(new_word)
        
        if word[0].isdigit():
            words.remove(word)
        
        if '&' in word:
            words.remove(word)

    return words


def word_parser(value):
    if ' ' in value:
        value = value.split(' ') # splits words on space into list
        new_value = double_check(value)
        return new_value

    if '#' in value:
        if any(x.isupper() for x in value):
            value = upper_check(value[1:]) # removes hashtag and checks for multiple uppercase
            new_value = double_check(value)
            return new_value
        else:    
            return value[1:]

    else:
        return value
