# with open("./topic-0.txt") as data_file:
# 	data = data_file.readlines()

# data_set1 = {}
# total_num = 0
# line_num  = len(data)
# for lines in data:
# 	a_line = lines.split()
# 	for number in a_line:
# 		if number in data_set1:
# 			data_set1[number]+=1
# 		else:
# 			data_set1[number]=1
# 		total_num+=1

# print(data_set1)

a = [1,2,3,4,5]

#print(a[0:5])

# with open("topic-0.txt") as datafile:
# 	data = datafile.readlines()
# 	data = data.split()

# print len(data)
from max_close import *

def Get_index_word_table():
	dict_idx_word = {}
	i = 0
	with open("./vocab.txt") as datafile:
		data = datafile.readlines()
	
	for lines in data:
		dict_idx_word[str(i)] = lines.replace('\n','')
		i=i+1

	return dict_idx_word 
#tb = Get_index_word_table()
#print tb

def Transfer_file(path):
	input_file = Read_Frequent_Pattern(path)
	index_word_table = Get_index_word_table()
	output = []
	for index, row in input_file.iterrows():
		pattern_word = []
		lens = len(row['pattern'])
		num_list  = row['pattern'][1:lens-1].replace("'","").replace(",","").split()
		#print num_list
		for i in num_list:
			pattern_word.append(index_word_table[i])
		output.append([row['support'],pattern_word])

	output = pd.DataFrame(output,columns = ['support', 'pattern'])
	output.to_csv(path,index = False)
	return output


#res = Transfer_file("./patterns/pattern-3.txt")
#print res
