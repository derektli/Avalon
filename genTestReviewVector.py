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


data_file = open('yelp_test_set/yelp_test_set_review.json')
enchant_dict = enchant.Dict("en_US")
user_dict = {}
business_dict = {}
word_dict = {}
num_user = 0
num_business = 0
num_word = 0
num_review = 0
num_out_review = 0

review_vec_file = open('official_test_review_matrix.txt', 'w')
business_table_file = open('official/official_business_table.txt', 'r')
user_table_file = open('official/official_user_table.txt', 'r')
word_table_file = open('official/official_word_table.txt', 'r')

for line in business_table_file:
    l = line.split()
    business_dict[l[1]] = int(l[0]) - 1 

for line in user_table_file:
    l = line.split()
    user_dict[l[1]] = int(l[0]) - 1

for line in word_table_file:
    l = line.split()
    word_dict[l[1]] = int(l[0]) - 1


for line in data_file:
    num_review = num_review + 1
    if num_review%1000 == 0:
        print "#review: ", num_review, num_out_review
    data = json.loads(line)
    
    bid = data['business_id'].encode('ascii','ignore')
    uid = data['user_id'].encode('ascii','ignore')

    if True:
        arr =  [0 for x in range(1721)]
        num_out_review = num_out_review + 1
        usefulness = 0
        arr[0] = usefulness
        review = _sanitize(data['text'].encode('ascii','ignore'))
        filtered_words = [w for w in review.split() if not w in nltk.corpus.stopwords.words('english')]
        for word in filtered_words:
            if enchant_dict.check(word):
                w = stem(word)
                if word_dict.has_key(w):
                    arr[word_dict[w]+1] = arr[word_dict[w]+1] + 1

        for i in range(len(arr)):
            review_vec_file.write("{0} ".format(arr[i]))
        review_vec_file.write("\n")
