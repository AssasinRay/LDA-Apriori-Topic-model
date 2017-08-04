#Preprocessing

def Generate_Dict():
	res = open("vocab.txt", "w")
	with open("paper.txt") as data_file:
		data = data_file.readlines()

	#print(data[0][5])
	check_unique = []

	for line in data:
		words = Process_title(line)
		for word in words:
			if word in check_unique:
				pass
			else:	check_unique.append(word)

	for item in check_unique:
  		res.write("%s\n" % item)

def Process_title(sentence):
	words = sentence.split()
	#print(words)
	return words[1:]

def Token_title(title, words):
	res = []
	unique_len = len(set(title))
	res.append(unique_len)
	unique = []
	for word in title:
		if not word in unique:
			elem =  str(words.index(word+'\n')) +":"+ str(title.count(word))
			res.append(elem)
			unique.append(word)
	return res

def Tokenize_Text():
	res = open("title.txt", "w")
	words = []

	with open("paper.txt") as data_file:
		data = data_file.readlines()

	with open("vocab.txt") as v:
		word = v.readlines()
		words.append(word)

	#print(words)

	tokens = []
	for line in data:
		title = Process_title(line)
		tokens.append(Token_title(title, words[0]))

	for t in tokens:
		#elem = '"' + str(t)[1:-1].replace(',', '').replace("'", '') + '"'
		elem = str(t)[1:-1].replace(',', '').replace("'", '')
		res.write("%s\n" % elem)


Generate_Dict()
Tokenize_Text()


