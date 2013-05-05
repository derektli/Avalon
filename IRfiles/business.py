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


data_file = open('yelp_training_set_business.json', 'r')
similarity_file = open('../latentProbabilities/output_business_word_matrix.txt', 'r')
enchant_dict = enchant.Dict("en_US")
user_dict = {}
business_dict = {}
word_dict = {}
num_user = 0
num_business = 0
num_word = 0
num_review = 0
arr = [["NA" for x in range(8)] for y in range(1000)]

business_file = open('business.csv', 'w')
business_table_file = open('official_business_table.txt', 'r')


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
        name = (data['name'].encode('ascii','ignore')).strip(',')
        lat = data['latitude']
        lon = data['longitude']
        review_count = data['review_count'] 
        star = data['stars']
        category = ((data['categories'][0]).encode('ascii','ignore')).strip(',')
        arr[business_dict[bid]][2] = name
        arr[business_dict[bid]][3] = lat
        arr[business_dict[bid]][4] = lon
        arr[business_dict[bid]][5] = star
        arr[business_dict[bid]][6] = review_count
        arr[business_dict[bid]][7] = category

for i in range(1000):
    if arr[i][7] == 'American (New)': 
        arr[i][7] = 'American'
    if arr[i][7] == 'American (Traditional)': 
        arr[i][7] = 'American'    
    if arr[i][7] == 'Burgers': 
        arr[i][7] = 'American'    
    if arr[i][7] == 'Steakhouses': 
        arr[i][7] = 'American'        
    if arr[i][7] == 'Bars': 
        arr[i][7] = 'Nightlife'    
    if arr[i][7] == 'Wine Bars': 
        arr[i][7] = 'Nightlife'    
    if arr[i][7] == 'Pubs': 
        arr[i][7] = 'Nightlife'   
    if arr[i][7] == 'Chinese': 
        arr[i][7] = 'Asian' 
    if arr[i][7] == 'Thai': 
        arr[i][7] = 'Asian' 
    if arr[i][7] == 'Food': 
        arr[i][7] = 'Asian' 
    if arr[i][7] == 'Sushi Bars': 
        arr[i][7] = 'Asian' 
    if arr[i][7] == 'Asian Fusion': 
        arr[i][7] = 'Asian'    
    if arr[i][7] == 'Barbeque': 
        arr[i][7] = 'American'    
    if arr[i][7] == 'Active Life': 
        arr[i][7] = 'Arts & Entertainment'    
    if arr[i][7] == 'Restaurants': 
        arr[i][7] = 'American'    
    if arr[i][7] == 'Vietnamese': 
        arr[i][7] = 'Asian'    
    if arr[i][7] == 'Pizza': 
        arr[i][7] = 'Italian'    
    if arr[i][7] == 'Bakeries': 
        arr[i][7] = 'Breakfast & Brunch'    
    if arr[i][7] == 'Seafood': 
        arr[i][7] = 'American'    
    if arr[i][7] == 'Greek': 
        arr[i][7] = 'Italian'    
    
    
    
    

category_dict = {}
numCategory = 0
numEtc = 0
business_file.write("similarity1,similarity2,name,latitude,longitude,stars,review_count,category\n")
for i in range(1000):
    for j in range(7):
        if j>0:
            business_file.write(",")
        business_file .write("{0}".format(arr[i][j]))

    #Category
    business_file.write(",")
    
    k = 0;
    for j in range(1000):
        if arr[j][7] == arr[i][7]:
            k = k + 1
    if k>=10:
        if not category_dict.has_key(arr[i][7]):
            category_dict[arr[i][7]] = 1
            numCategory = numCategory + 1
        business_file .write("{0}".format(arr[i][7]))
    else:
        business_file .write("etc")
        numEtc = numEtc + 1
    business_file.write("\n")

print numCategory
print numEtc
print category_dict
