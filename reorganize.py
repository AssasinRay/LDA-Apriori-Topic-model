
def Process_title(sentence):
	words = sentence.split()
	#print(words)
	return words[1:]

def Process_word(word):
	topic_num = int(word.split(':')[1])
	term_index = word.split(':')[0].lstrip('0').lstrip()
	#term_index = int(word.split(':')[0].lstrip('0'))
	return [topic_num, term_index]

def Reorgnize_by_Topic():
	topic0 = open("topic-0.txt", "w")
	topic1 = open("topic-1.txt", "w")
	topic2 = open("topic-2.txt", "w")
	topic3 = open("topic-3.txt", "w")
	topic4 = open("topic-4.txt", "w")
	dict_all = {}

	with open("./result/word-assignments.dat") as data_file:
		data = data_file.readlines()

	line_num = 1
	for line in data:
		words = Process_title(line)
		for word in words:
			topic_num = Process_word(word)[0]
			term_index = Process_word(word)[1]
			if not topic_num in dict_all:
				dict_all[topic_num] = {}
			if not line_num in dict_all[topic_num]:
				dict_all[topic_num][line_num] = []
			dict_all[topic_num][line_num].append(term_index)
		line_num = line_num + 1

	dict0 = dict_all[0]
	dict1 = dict_all[1]
	dict2 = dict_all[2]
	dict3 = dict_all[3]
	dict4 = dict_all[4]

	for item in dict0:
		elem = str(dict0[item])[1:-1].replace(',', '').replace("'", '').lstrip()
   		topic0.write("%s\n" % elem)

   	for item in dict1:
		elem = str(dict1[item])[1:-1].replace(',', '').replace("'", '').lstrip()
   		topic1.write("%s\n" % elem)

   	for item in dict2:
		elem = str(dict2[item])[1:-1].replace(',', '').replace("'", '').lstrip()
   		topic2.write("%s\n" % elem)

   	for item in dict3:
		elem = str(dict3[item])[1:-1].replace(',', '').replace("'", '').lstrip()
   		topic3.write("%s\n" % elem)

   	for item in dict4:
		elem = str(dict4[item])[1:-1].replace(',', '').replace("'", '').lstrip()
   		topic4.write("%s\n" % elem)


Reorgnize_by_Topic()