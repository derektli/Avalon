
data_file = open('word.csv', 'r')
similarity_file = open('../latentProbabilities/output_word_business_matrix.txt', 'r')
word_file = open('new_word.csv', 'w')

lists = []

for line in data_file:
	lists.append(line)

i=1

word_file.write("{0}\n".format(lists[0]))

for line in similarity_file:
	l = line.split(',')
	print i
	s = lists[i].split(',')
	s[0] = l[1]
	s[1] = l[2]
	for j in range(8):
		if j>0:
			word_file.write(",")
		word_file .write("{0}".format(s[j]))
	word_file.write("\n")
	i = i + 1
	
