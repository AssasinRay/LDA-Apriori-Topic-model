import pandas as pd
from apriori import Line_Contain_pattern
import ast

def Read_Frequent_Pattern(path):
	table = pd.read_csv(path, names = ['support', 'pattern'],sep = '\t')
	#table = pd.read_csv(path)
	return table

def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))

def Find_closed_Pattern(path):
	table = Read_Frequent_Pattern(path)
	for index,row in table.iterrows():
		support = row['support']
		pattern = row['pattern']
		#pattern = table.get_value(index,'pattern')
		for later_idx, later_row in table[index+1:].iterrows():
			later_support = later_row['support']
			later_pattern = later_row['pattern']
			#later_pattern = table.get_value(later_idx,'pattern')

			later_pattern_list = ast.literal_eval(later_pattern)
			pattern_list = ast.literal_eval(pattern)

			pair1 = [support,pattern_list]
			pair2 = [later_support,later_pattern_list]

			if Closed_pattern_check(pair1,pair2)==True:
				table.drop(table.index[[index]],inplace= True)
	return table

def Closed_pattern_check(pair1, pair2):
	support1 = pair1[0]
	support2 = pair2[0]
	list1	=  pair1[1]
	list2   = pair2[1]

	if support2 == support1 and (contains_sublist(list2,list1) or contains_sublist(list1,list2)):
		return True
	return False

def Find_max_Pattern(path):
	table = Read_Frequent_Pattern(path)
	for index,row in table.iterrows():
		support = row['support']
		pattern = row['pattern']
		#pattern = table.get_value(index,'pattern')
		for later_idx, later_row in table[index+1:].iterrows():
			later_support = later_row['support']
			later_pattern = later_row['pattern']
			#later_pattern = table.get_value(later_idx,'pattern')

			later_pattern_list = ast.literal_eval(later_pattern)
			pattern_list = ast.literal_eval(pattern)

			#if Line_Contain_pattern(later_pattern_list,pattern_list) == True or Line_Contain_pattern(pattern_list,later_pattern_list) == True:
			if contains_sublist(later_pattern_list,pattern_list) or contains_sublist(pattern_list,later_pattern_list):
				#print True
				table.drop(table.index[[index]],inplace= True)
	return table



#res = Find_max_Pattern("./patterns/pattern-0.txt")
#print res