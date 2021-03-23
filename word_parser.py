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


def word_parser(value):
    if ' ' in value:
        return value.split(' ')

    if '#' in value:
        if any(x.isupper() for x in value):
            value = upper_check(value[1:])
            return value
        else:    
            return value

    else:
        return value