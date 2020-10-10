'''
This script strip all the punctuations and convert the uppercase to lowercase at the beginning of a sentence
but remain the abraviations like HKUST/UMD/HKPOLYU in uppercases
'''
# -*- coding: utf-8 -*-

import re
import string
import pandas
import numpy as np
from numpy import random

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([a-z][.][a-z][.](?:[a-z][.])?)"
websites = "[.](com|net|org|io|gov|me|edu)"
digits = "([0-9])"

pre_suffix = ["Mr","St","Mrs","Ms","Dr","Prof","Capt","Cpt","Lt","Mt", "Inc","Ltd","Jr","Sr","Co"]

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub("http://www.","http://www<prd>",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text) 
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    if "e.g." in text: text = text.replace("e.g.","e<prd>g<prd>") 
    if "i.e." in text: text = text.replace("i.e.","i<prd>e<prd>") 
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")

    sentences = text.split("<stop>")

    sentences = sentences[:-1]

    return sentences

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def tokenize(text):
    raw = text.split()
    tokens = []
    for word in raw:
        word = word.strip()

        if ('\'s' in word):
            token = [''.join(c for c in word if c not in string.punctuation)[:-1], '\'s']
        else:
            token = [''.join(c for c in word if c not in string.punctuation)]
        
        if is_number(token[0]):
            tokens += token
        elif not token[0].isupper() and not (token[0] in pre_suffix):
            token[0] = token[0].lower()
            tokens += token
    return tokens
        
if __name__ == "__main__":
    # load file
    df = pandas.read_pickle("parsed_10K.pkl")
    df.dropna()

    # Item 1. Business.
    # ITEM 1A. RISK FACTORS
    # Item 7. Management\'s Discussion and Analysis of Financial Condition and Results of Operations.

    raw = np.append(df['Item1'].values, df['Item1A'].values)
    raw = np.append(raw, df['Item7'].values)
    random.shuffle(raw)

    corpus = []
    invalid = []

    for elem in raw:
        sentences = split_into_sentences(elem)
        if len(sentences) > 2:
            sentences.pop(0)
            sentences.pop(0)
            tokens = [tokenize(sent) for sent in sentences]
            corpus += tokens
            corpus += [['<eod>']]
        #else:
            #print('{} is invalid.'.format(i))
            #invalid.append(' '.join([col_name, str(i)]))
    
    # write the preprocessed data into a .txt file
    with open("training_corpus.txt", "w") as w_f:
        for sent in corpus:
            w_f.write(' '.join(sent))
            w_f.write('\n')
    
    #with open("invalid.txt", "w") as w_f:
    #    w_f.write('\n'.join(invalid))
