import json
from pprint import pprint
from stemming.porter2 import stem
import re
import nltk
import enchant

def _sanitize(title):
    title = title.lower()
    
    title = re.sub(r'[^a-zA-Z ]',r'',title)

    title = re.sub(r'\s+',r' ', title)

    title = re.sub(r'^\s+|\s+$',r'',title)

    return title


data_file = open('yelp_training_set_review.json')
enchant_dict = enchant.Dict("en_US")
user_dict = {}
business_dict = {}
word_dict = {}
num_user = 0
num_business = 0
num_word = 0
num_review = 0

user_to_word_file = open('user_to_word.txt', 'w')
business_to_word_file = open('business_to_word.txt', 'w')
user_table_file = open('user_table.txt', 'w')
business_table_file = open('business_table.txt', 'w')
word_table_file = open('word_table.txt', 'w')

for line in data_file:
    num_review = num_review + 1
    if num_review%1000 == 0:
        print "#review: ", num_review
    data = json.loads(line)
    
    bid = data['business_id'].encode('ascii','ignore')
    if not business_dict.has_key(bid):
        business_dict[bid] = num_business
        business_table_file.write("{0} {1}\n".format(bid, num_business))
        num_business = num_business + 1
    
    uid = data['user_id'].encode('ascii','ignore')
    if not user_dict.has_key(uid):
        user_dict[uid] = num_user
        user_table_file.write("{0} {1}\n".format(uid, num_user))
        num_user = num_user + 1
        
    #print "\n\n\n Sanitized review:\n"
    review = _sanitize(data['text'].encode('ascii','ignore'))
    #print review 
    #print "\n\n\n Filtered review:\n"
    
    filtered_words = [w for w in review.split() if not w in nltk.corpus.stopwords.words('english')]
    for word in filtered_words:
        if enchant_dict.check(word):
            w = stem(word)
            if not word_dict.has_key(w):
                word_dict[w] = (num_word, word)
                word_table_file.write("{0} {1}\n".format(word, num_word))
                num_word = num_word + 1
            user_to_word_file.write("{0} {1}\n".format(user_dict[uid], word_dict[w][0]))
            business_to_word_file.write("{0} {1}\n".format(business_dict[bid], word_dict[w][0]))
            
print "#business: ", num_business
print "#user: ", num_user
print "#words: ", num_word

