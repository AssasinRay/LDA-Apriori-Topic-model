from __future__ import division
import math
from max_close import *
from reorganize import *
from max_close import *
import ast
from apriori import *
from decimal import *

#from Main import *


topic_paths = ['topic-0.txt','topic-1.txt','topic-2.txt','topic-3.txt','topic-4.txt'] 
freq_pattern_paths = ["./patterns/pattern-0.txt","./patterns/pattern-1.txt","./patterns/pattern-2.txt","./patterns/pattern-3.txt","./patterns/pattern-4.txt"]
def Get_topic_sets(paths):
	data = [[],[],[],[],[]]
	i = 0
	for path in paths:
		with open(path) as data_file:
			line = data_file.readlines()
			#print line
			for numbers in line:
				numbers = numbers.split()
				for number in numbers:
					#data[i].append(int(number))
					data[i].append(number)
		i=i+1

	for i in xrange(5):
		data[i] = set(data[i])

	return data


def Get_topic_table(paths):
	topics = {}
	i=0
	for path in paths:
		topics[i] = []
		with open(path) as datafile:
			lines = datafile.readlines()
			for numbers in lines:
				numbers = numbers.split()
				topics[i].append(numbers)
		i=i+1
	return topics

def Get_title_table(path):
	res = {}
	i=0
	with open(path) as datafile:
		data = datafile.readlines()
	for line in data:
		words = Process_title(line)
		res[i] = []
		for word in words:
			term_index = Process_word(word)[1]
			res[i].append(term_index)
		i=i+1
	return res

def Get_D(topic_paths):
	D = [0,0,0,0,0]
	for i in  xrange(5):
		D[i] = sum(1 for line in open(topic_paths[i]))
	return D


def Calulate_Purity(freq_path, topic_paths, title_path,t):
	table = Read_Frequent_Pattern(freq_path)       #read pattern-i  support, pattern
	topic_termIdx = Get_topic_sets(topic_paths)		#get a list of unique termidx  eg a[0]= all term index in tpoic0 topict_termIdx= [['5',...],,,,,]
	topic_table   = Get_topic_table(topic_paths)  #get a dict of topics dict[0]= [lines:[numbers]]
	D = Get_D(topic_paths)							#get a list of line number (D[i])

	res = []								#get result of all pattern_purity_set in table
											#res[i]= [pattenr[i], [p_0,p_1,p_2,p_3,p_4]] 
	Dt_t = Get_Dt_t(topic_termIdx,Get_title_table(title_path))			#Dt_t[3,4] = D(t,t') where t= 3 t'=4
	for index,row in table.iterrows():
		pattern = row['pattern']					#calculate purity
		pattern = ast.literal_eval(pattern)
		purity = Calulate_Purity_util(pattern,t,D,Dt_t,topic_table)
		res.append([pattern,purity])
	return res

def Get_Frequency(pattern,t,topic_table):
	count = 0
	for line in topic_table[t]:
		if contains_sublist(line,pattern) == True:
			count=count+1
	return count


def Get_Dt_t(terms_list, title_table):
	res ={}
	#print terms_list[1]
	for t in xrange(5):
		for t_prime in xrange(5):
			if t==t_prime: continue
			res[(t,t_prime)] = 0
			if t_prime < t:
				res[(t,t_prime)] = res[(t_prime,t)]
				continue
			for line,title in title_table.iteritems():
				#pass
				flag = False
				#print line, title
				for word in title:
					#print word
					if word in terms_list[t]: #or word in terms_list[t_prime]:
						flag = True
						break
				if flag == True:
					res[(t,t_prime)]+=1
	return res



def Calulate_Purity_util(pattern,t,D,Dt_t,topic_table):
	f_t_p = Get_Frequency(pattern,t,topic_table)

	
	#print(pattern)

	#print "f_t_p", f_t_p
	if f_t_p == 0: f_t_p = 1
	#print "Dt" , D[t]

	#print "f--p", f_t_p
	one = Decimal(f_t_p/D[t])
	#print "one",one
	res = math.log(float(f_t_p/D[t]),2)
	#print "f_t_p/dt" , one
	test1 = math.log(one,2)
	#print "test1", math.log(one,2)
	#print "one " , res
	second = 0
	for t_prime in xrange(5):
		if t_prime==t: continue
		f_t_prime_p = Get_Frequency(pattern,t_prime,topic_table)
		#print "f_t_prime_p",f_t_prime_p

		divider= (f_t_p + f_t_prime_p)
		#print "sum", divider
		#divisor = Get_D(t,t_prime,terms_list)
		divisor = Dt_t[t,t_prime]
		#print "Dt_t", divisor
		#print divisor
		val = float(float(divider)/float(divisor))
		#print val
		#print "f_t_p + f_t_prime_p / Dtt",second
		second = max(val,second)
		#print second

	#print "second",second
	#print "test2", math.log(second,2)
	res = res - math.log(second,2)
	#print res
	return res


def Sort_by_combo(freq_path, topic_paths, title_path,t):
	table = Read_Frequent_Pattern(freq_path)
	pure_pair = Calulate_Purity(freq_path, topic_paths, title_path,t)
	#print pure_pair
	support =[]
	clean_data = Process_data(freq_path)
	for index,row in table.iterrows():
		pure_val = pure_pair[index][1]
		#print pure_val
		#print row['support']
		pure_val_3  = pow(pure_val,3)
		support.append( [row['pattern'],row['support'] * pure_val_3,pure_val ])

	pairs = list(reversed(sorted(support,key=lambda x: x[1])))
	return pairs

#test = Calulate_Purity("./patterns/pattern-1.txt",topic_paths,"./title.txt",1)
# test = Sort_by_combo("./patterns/pattern-1.txt",topic_paths,"./title.txt",1)
# print test
# fo = open("./purity/purity-1.txt","w")

# for pair in test:
# 	support = pair[1]
# 	freq    = pair[0]
# 	elem = str(support) + "\t" + str(freq)
# 	fo.write("%s\n" % elem)

#Transfer_file("./purity/purity-1.txt")
#D = Get_D(topic_paths)
#print res

#s = Get_Dt_t(Get_topic_sets(topic_paths),Get_title_table("/Users/Zhuangyiwei/Desktop/fall16/412/yizhuan2_assign3/title.txt"))
#print s

#res = Calulate_Purity_util(['38'],1,D,s,Get_topic_table(topic_paths))

#tl = Get_topic_sets(topic_paths)
#print len(tl[0]), len(tl[1]),len(tl[2]),len(tl[3]),len(tl[4])
#terms_list= Get_topic_sets(topic_paths)
#print terms_list[2]
#print  "4" in terms_list[2]