import re
def apriori(data_path, minSup):

	structure_data = Process_data(data_path)
	freq_table = Get_Freq_all(structure_data)

	len_num = len(structure_data)
	print("total numer of data: " + str(len_num))
	minSup_num = minSup * len_num

	PrunePattern1 = Get_Oneitem_set(freq_table, minSup_num)
	#print(PrunePattern1)
	cur_key = PrunePattern1
	all_pattern = []

	while cur_key != []:
		#counts = Get_Counts(structure_data, cur_key)
		#print(counts)
		PrunePattern = Get_Prune_Pattern(cur_key,minSup_num,structure_data)
		for item in PrunePattern:
			all_pattern.append(item)

		cur_key = Get_apriori(PrunePattern)

	return all_pattern

def Get_apriori(PrunePattern):
	next_pattern = []
	for item1 in PrunePattern:
		for item2 in PrunePattern:
			if item1 == item2:
				continue

			new_item = []
			for number in item1:
				if number not in new_item:
					new_item.append(number)

			for number in item2:
				if number not in new_item:
					new_item.append(number)

			new_item.sort()

			if new_item not in next_pattern:
				next_pattern.append(new_item)

	return next_pattern

def Get_Prune_Pattern(cur_pattern, minSup_num, data,counts=[]):
	for item in cur_pattern[:]:
		num = 0
		for line in data:
			if Find_key_line(item,line) == True:
				num = num+1
		if num < minSup_num:
			cur_pattern.remove(item)

	return cur_pattern

def Find_key_line(item,line):
	for number in item:
		if number not in line:
			return False
	return True

def Get_Counts(data,cur_pattern):
	count = 0
	pattern_len = len(cur_pattern)
	for line in data:
		if Line_Contain_pattern(line, cur_pattern) == True:
			count=count + 1		

	return count

def Line_Contain_pattern(line, pattern):
	if len(pattern) == 1 : return pattern[0] in line

	else:
		for i in xrange(len(line)):
			for j in xrange(i+1,len(line)+1):
				if pattern == line[i:j]:
					return True
	return False


def Get_Oneitem_set(freq_table,minSup_num):
	res = []
	for number,count in freq_table.iteritems():
		if count >= minSup_num:
			res.append([number])
	res.sort()
	return res


def Get_Freq_all(structure_data):
	freq_table = {}
	for line in structure_data:
		for number in line:
			if number in freq_table:
				freq_table[number] +=1
			else:
				freq_table[number] =1
	return freq_table


def Process_data(data_path):
	res = []
	with open(data_path) as data_file:
		data = data_file.readlines()

	for line in data:
		res.append(line.split())

	return res

#res = apriori("./topic-0.txt",0.05)
#print res
#structure_data = Process_data("./topic-0.txt")
#res = Get_Counts(structure_data,['67'])
#print(res)
#[['1010'], ['1022'], ['1043'], ['1044'], ['105'], ['11'], ['1129'], ['1183'], ['1261'], ['138'], ['149'], ['150'], ['162'], ['174'], ['177'], ['181'], ['188'], ['190'], ['191'], ['194'], ['205'], ['21'], ['211'], ['225'], ['233'], ['234'], ['248'], ['25'], ['255'], ['26'], ['27'], ['28'], ['284'], ['288'], ['298'], ['299'], ['32'], ['323'], ['325'], ['326'], ['330'], ['339'], ['359'], ['36'], ['362'], ['374'], ['376'], ['382'], ['390'], ['397'], ['418'], ['424'], ['43'], ['439'], ['443'], ['45'], ['453'], ['458'], ['479'], ['481'], ['497'], ['56'], ['590'], ['6'], ['60'], ['625'], ['627'], ['66'], ['67'], ['690'], ['718'], ['755'], ['767'], ['838'], ['84'], ['88'], ['893'], ['909'], ['946'], ['973'], ['982'], ['987'], ['105', '190'], ['105', '25'], ['190', '25'], ['190', '376'], ['190', '397'], ['234', '6'], ['25', '6'], ['25', '67'], ['284', '298'], ['326', '6'], ['6', '60'], ['6', '67']]

