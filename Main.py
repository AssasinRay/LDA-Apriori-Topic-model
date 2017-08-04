from sys import argv
from apriori import *
from max_close import *
from re_rank   import *
from operator import itemgetter
import pandas as pd
command = "python Main.py [min-sup]"

min_sup = 0.01
in_paths = ["./topic-0.txt","./topic-1.txt","./topic-2.txt","./topic-3.txt","./topic-4.txt"]
out_paths = ["./patterns/pattern-0.txt","./patterns/pattern-1.txt","./patterns/pattern-2.txt","./patterns/pattern-3.txt","./patterns/pattern-4.txt"]
max_out_paths = ["./max/max-0.txt","./max/max-1.txt","./max/max-2.txt","./max/max-3.txt","./max/max-4.txt"]
closed_out_paths = ["./closed/closed-0.txt","./closed/closed-1.txt","./closed/closed-2.txt","./closed/closed-3.txt","./closed/closed-4.txt"]
puriry_out_paths = ["./purity/purity-0.txt","./purity/purity-1.txt","./purity/purity-2.txt","./purity/purity-3.txt","./purity/purity-4.txt",]

def Get_index_word_table():
	dict_idx_word = {}
	i = 0
	with open("./vocab.txt") as datafile:
		data = datafile.readlines()
	
	for lines in data:
		dict_idx_word[str(i)] = lines.replace('\n','')
		i=i+1

	return dict_idx_word 

def Transfer_file(path):
	input_file = Read_Frequent_Pattern(path)
	index_word_table = Get_index_word_table()
	output = []
	#print input_file
	for index, row in input_file.iterrows():
		pattern_word = []
		#print row['pattern']
		lens = len(row['pattern'])
		num_list  = row['pattern'][1:lens-1].replace("'","").replace(",","").split()
		#print num_list
		for i in num_list:
			pattern_word.append(index_word_table[i])
		output.append([row['support'],pattern_word])

	output = pd.DataFrame(output,columns = ['support', 'pattern'])
	output.to_csv(path+ ".phrase",index = False)
	return output

def Transfer_file_c(path):
	input_file = pd.read_csv(path,header=1,names = ['support', 'pattern'])
	index_word_table = Get_index_word_table()
	output = []
	#print input_file
	for index, row in input_file.iterrows():
		pattern_word = []
		#print row['pattern']
		lens = len(row['pattern'])
		num_list  = row['pattern'][1:lens-1].replace("'","").replace(",","").split()
		#print num_list
		for i in num_list:
			pattern_word.append(index_word_table[i])
		output.append([row['support'],pattern_word])

	output = pd.DataFrame(output,columns = ['support', 'pattern'])
	output.to_csv(path+ ".phrase",index = False)
	return output

def Transfer_file_p(path):
	input_file = pd.read_csv(path,header=0,names = [ 'purity','support', 'pattern'],sep='\t')
	index_word_table = Get_index_word_table()
	output = []
	#print input_file
	for index, row in input_file.iterrows():
		pattern_word = []
		#print row['pattern']
		lens = len(row['pattern'])
		num_list  = row['pattern'][1:lens-1].replace("'","").replace(",","").split()
		#print num_list
		for i in num_list:
			pattern_word.append(index_word_table[i])
		output.append([row['purity'],row['support'],pattern_word])

	output = pd.DataFrame(output,columns = ['purity','support_combo', 'pattern'])
	output.drop('support_combo', 1, inplace =True)
	output.to_csv(path + ".phrase",index = False)
	return output

def main_freq(input_file_path,output,min_sup):
	fo = open(output,'w')
	freq_pattern = apriori(input_file_path, min_sup)
	#print(freq_pattern)
	freq_pattern_support =[]
	clean_data = Process_data(input_file_path)
	for pattern in freq_pattern:
		freq_pattern_support.append( [pattern,Get_Counts(clean_data,pattern)])
		
	#print(freq_pattern_support)
	pairs = list(reversed(sorted(freq_pattern_support,key=lambda x: x[1])))
	#print(pairs)
	for pair in pairs:
		support = pair[1]
		freq    = pair[0]
		elem = str(support) + "\t" + str(freq)
		fo.write("%s\n" % elem)

def main_max(in_path,out_path):
	max_pattern = Find_max_Pattern(in_path)
	max_pattern = max_pattern[1:]
	#max_pattern = pd.DataFrame(out_path,columns = ['support', 'pattern'])
	#print max_pattern
	max_pattern.to_csv(out_path,index = False)

def main_closed(in_path,out_path):
	closed_pattern = Find_closed_Pattern(in_path)
	closed_pattern.to_csv(out_path,index = False)

def main_purity(in_path,out_path,i):
	test = Sort_by_combo(in_path,in_paths,"./title.txt",i)
	fo = open(out_path,"w")
	#fo.write("%s\n" % "pure 	support_combo 	patterns")
	for pair in test:
		support = pair[1]
		freq    = pair[0]
		pure_val = pair[2]
		elem =  str(pure_val) +"\t"+  str(support) + "\t"+ str(freq) 
		fo.write("%s\n" % elem)




def main(min_sup):
	i=0
	print "generate frequent patterns for min_sup = ", str(min_sup)
	for path in in_paths:
		main_freq(path,out_paths[i],min_sup)
		i=i+1

	print "generate closed patterns"
	for i in xrange(5):
		main_closed(out_paths[i],closed_out_paths[i])

	print "generate max patterns"
	for i in xrange(5):
		main_max(out_paths[i],max_out_paths[i])

	print "generate purity patterns"
	for i in xrange(5):
		main_purity(out_paths[i],puriry_out_paths[i],i)

	print "Transfer term_index to names"
	for i in xrange(5):
		Transfer_file_c(closed_out_paths[i])
		Transfer_file_c(max_out_paths[i])
		Transfer_file_p(puriry_out_paths[i])
		Transfer_file(out_paths[i])
	return 

main(min_sup)



