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
arr = [[0 for x in range(1000)] for y in range(1000)]

business_to_user_file = open('official_business_user_matrix.txt', 'w')
business_table_file = open('official_business_table.txt', 'r')
user_table_file = open('official_user_table.txt', 'r')

for line in business_table_file:
    l = line.split()
    business_dict[l[1]] = int(l[0]) - 1 

for line in user_table_file:
    l = line.split()
    user_dict[l[1]] = int(l[0]) - 1


for line in data_file:
    num_review = num_review + 1
    if num_review%1000 == 0:
        print "#review: ", num_review
    data = json.loads(line)
    
    bid = data['business_id'].encode('ascii','ignore')
    uid = data['user_id'].encode('ascii','ignore')

    if user_dict.has_key(uid) and business_dict.has_key(bid):
        star = data['stars']
        arr[business_dict[bid]][user_dict[uid]] = star

for i in range(1000):
    for j in range(1000):
        if j>0:
            business_to_user_file.write(",")
        business_to_user_file.write("{0}".format(arr[i][j]))
    business_to_user_file.write("\n")