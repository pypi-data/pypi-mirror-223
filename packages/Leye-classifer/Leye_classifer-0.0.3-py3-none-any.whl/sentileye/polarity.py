import csv 
import os
import re
import ast
import pandas as pd
from csv import reader
from sentileye.booster import booster
from sentileye.emoticon import emoticon
from importlib import resources 
import io


def get_user_data():
    message = 'Hello, you are welcome to SentiLEYE sentiment classifier'
    print('{:^80}'.format(message))
    #Read in file to classify
    user = input('Do you have a csv file to classify? Enter yes/no ').lower()
    print("\n")
    if user == 'yes' or user == 'y':
        message1 = '*****Please read instructions carefully*****'
        print('{:^80}'.format(message1))
        print("\n")
        print('''
              1. Load file in .csv format
              2. Input csv file header as text - This means document or sentences to classify should have column name = text
              ''')
        print("\n")
        fileinput = str(input('Your filename - kindly include .csv extension:       '))
        print("\n")
        data = pd.read_csv(fileinput)
        data = pd.DataFrame(data['text']) 
    elif user == 'no' or user == 'n':
        print("\n")
        message = [input('Do you want to classify raw text or sentence? If yes, enter text here     ')]
        print("\n")
        data = pd.DataFrame(list(reader(message)))
        data['text'] = data[0] 
        data = pd.DataFrame(data['text']) 
    elif user != 'yes' or user != 'y' or user != 'no' or user != 'n':
        raise ValueError('Please enter yes or no')
    else:
        raise NameError('Sorry, you need a csv file or text')
   
    return data



with resources.path("sentileye", "emotion_new.csv") as data1:
    emotion_df = pd.read_csv(data1)
    emotion = dict(zip(emotion_df.term, emotion_df.score))

with resources.path("sentileye", "sentileye_list.csv") as data2:
    sentileye_df = pd.read_csv(data2)
    sentileye = dict(zip(sentileye_df.term, sentileye_df.score))

with resources.path("sentileye", "slang.csv") as data3:
    slang_df = pd.read_csv(data3)
    slang = dict(zip(slang_df.term, slang_df.score))

with resources.path("sentileye", "neg.txt") as dat:
    neg = ast.literal_eval(dat.read_text())

with resources.path("sentileye", "neg1.txt") as dat1:
    neg1 = ast.literal_eval(dat1.read_text())

    
# Regular expression for finding contractions
contractions_re=re.compile('(%s)' % '|'.join(neg.keys()))

# Function for expanding contractions
def expand_contractions(text,contractions_dict=neg):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, text)

# Regular expression for finding contractions if punctuation exist 
contractions_re1=re.compile('(%s)' % '|'.join(neg1.keys()))

# Function for expanding contractions
def expand_contractions_punct(text,contractions_dict=neg1):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re1.sub(replace, text)

# Regular expression for finding slang
contractions_re_slang = re.compile('('+'|'.join(slang.keys())+')')

# Function for expanding contractions
def expand_slang(text,contractions_dict=slang):
    def replace(match): 
        return contractions_dict[match.group(0)]
    return contractions_re_slang.sub(replace, text)

def get_score(s):
    value = 0
    result = 0
    negation = 0
    booster_word_count = 0
    pattern = '('+'|'.join(emotion.keys())+')'#Regular expression pattern 
    
    #sum values of exact word matched 
    for z in s.split():
        if z in sentileye:
            value += int(sentileye[z])
        elif z in re.findall(pattern, s):
            value += int(emotion[z])
        elif z in emoticon:
            value += int(emoticon[z])                     
                   
        if booster_word_count > 0 and value != 0: 
            value = value * 2
            booster_word_count -= 1
        if negation > 0 and value == 0: 
            value = 0
        if negation > 0 and value != 0: 
            value = -1 * value
            negation -= 2

        if z in booster:
            booster_word_count += 2
        elif z in ["no", "not", "but", "however", "nothing", "meanwhile", "yet", "without", "witout", "never", "although"]:
            negation += 2
   
        
        if negation >= 2:
            result -= 1  
        
    result += value       
    return result

def result():
    data = get_user_data()
    data['text'] = data['text'].apply(lambda x: " ".join(x.lower() for x in x.split()))
    # Expanding Contractions in the tweets
    data['text'] = data['text'].apply(lambda x:expand_contractions(x)) 
    # Expanding Contractions in the tweets if punctuation exist 
    data['text']=data['text'].apply(lambda x:expand_contractions_punct(x))
    # Expanding slangs
    data['text']=data['text'].apply(lambda x:expand_slang(x))
    data['score'] = data['text'].apply(lambda x: get_score(x))
    data['class'] = data['score'].apply(lambda x: 'positive' if x > 0
                                        else('neutral' if x == 0
                                             else 'negative'))
    data.to_csv('sentileyeresult.csv')
    return print(data)
