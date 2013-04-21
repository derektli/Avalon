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


data_file = open('yelp_training_set_review.json', 'r')
similarity_file = open('../latentProbabilities/output_word_business_matrix.txt', 'r')
enchant_dict = enchant.Dict("en_US")
word_dict = {}
business_dict = {}
num_user = 0
num_business = 0
num_word = 0
num_review = 0
arr = [['NA', 'NA', 'NA', 0, 0.0, 0, 0, 0] for y in range(1720)]

word_file = open('word.csv', 'w')
business_table_file = open('official_business_table.txt', 'r')
word_table_file = open('official_word_table.txt', 'r')

for line in word_table_file:
    l = line.split()
    word_dict[stem(l[1])] = int(l[0]) - 1 

for line in business_table_file:
    l = line.split()
    business_dict[l[1]] = int(l[0]) - 1 

#load similarity 
i = 0
for line in similarity_file:
    l = (line.strip('\n')).split(',')
    arr[i][0] = l[1]
    arr[i][1] = l[2]
    i = i + 1
    
for line in data_file:
    num_review = num_review + 1
    if num_review%1000 == 0:
        print "#review: ", num_review
    data = json.loads(line)
    
    bid = data['business_id'].encode('ascii','ignore')
    
    if business_dict.has_key(bid):
        review = _sanitize(data['text'].encode('ascii','ignore'))
        filtered_words = [w for w in review.split() if not w in nltk.corpus.stopwords.words('english')]
        temp_dict = {}
        for word in filtered_words:
            if enchant_dict.check(word):
                w = stem(word)
                if word_dict.has_key(w) and (not temp_dict.has_key(w)):
                    temp_dict[w] = 1
                    name = word
                    star = data['stars']
                    funny_vote = data['votes']['funny']
                    useful_vote = data['votes']['useful']
                    cool_vote = data['votes']['cool']

                    arr[word_dict[w]][2] = name
                    arr[word_dict[w]][3] = arr[word_dict[w]][3] + 1
                    arr[word_dict[w]][4] = arr[word_dict[w]][4] + star
                    arr[word_dict[w]][5] = arr[word_dict[w]][5] + useful_vote
                    arr[word_dict[w]][6] = arr[word_dict[w]][6] + funny_vote
                    arr[word_dict[w]][7] = arr[word_dict[w]][7] + cool_vote

                    #print arr[word_dict[w]]
        
word_file.write("similarity1,similarity2,name,review_count,average_stars,useful_count,funny_count,cool_count\n")
for i in range(1720):
    arr[i][4] = float(arr[i][4])/float(arr[i][3])
    for j in range(8):
        if j>0:
            word_file.write(",")
        word_file .write("{0}".format(arr[i][j]))
    word_file.write("\n")
    