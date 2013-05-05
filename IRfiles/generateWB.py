data_file = open('business_word_matrix.txt', "r")
out_file = open('word_business_matrix.txt', "w")
for line in data_file:
	l = line.split()
	out_file.write("{0} {1} {2}\n".format(l[1], l[0], l[2]))
