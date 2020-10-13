# import time
# import psycopg2
# from pytrends.request import TrendReq
import pickle
import datetime
import textdistance
import pandas as pd
from fuzzywuzzy import process
from clean_db_names import clean_list, clean_word
from gsearch_comparison import compare_search
# from matching_utils import RatcliffObershelp, Levenshtein, edit_based, token_based
from matching_utils import edit_based, token_based

# load suppliers names from DB to compare with
match_against = pd.read_csv('supplier_db.csv')

# load input suppliers names
input_list = pd.read_csv('supplier_list.csv')


# compares a str to a list of strs and return the best match
def RatcliffObershelp(str1, match_against):
	best_match = ['',0]
	str_comparison = [[x,textdistance.ratcliff_obershelp(str1,x)] for x in match_against]
	for item in str_comparison:
		if item[1] > best_match[1]:
			best_match = item

	return best_match

def Levenshtein(str1, match_against):
	best_match = ['',10000000]
	str_comparison = [[x,textdistance.levenshtein(str1,x)] for x in match_against]
	for item in str_comparison:
		if item[1] < best_match[1]:
			best_match = item

	return best_match


#################################################

def return_value(index_list, array):
	return array.loc[array.clean_name == index_list].original_name.iloc[0]

# clean stopwords from match_against
match_against_clean = clean_list(match_against.vendor_name)

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Levenshtein')

input_list['Levenshtein'] = input_list.supplier_name.apply(lambda x: edit_based(list(match_against_clean.clean_name), clean_word(x), textdistance.levenshtein))
input_list['Levenshtein_score'] = input_list.Levenshtein.apply(lambda x: x[1])
input_list['Levenshtein'] = input_list.Levenshtein.apply(lambda x: return_value(x[0],match_against_clean))


now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - RatcliffObershelp')

input_list['RatcliffObershelp'] = input_list.supplier_name.apply(lambda x: token_based(clean_word(x),list(match_against_clean.clean_name)),textdistance.ratcliff_obershelp)
input_list['RatcliffObershelp_score'] = input_list.RatcliffObershelp.apply(lambda x: x[1])
input_list['RatcliffObershelp'] = input_list.RatcliffObershelp.apply(lambda x: return_value(x[0],match_against_clean))

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - FuzzyWuzzy')

input_list['FuzzyWuzzy'] = input_list.supplier_name.apply(lambda x: list(process.extractOne(clean_word(x),list(match_against_clean.clean_name))))
input_list['FuzzyWuzzy_score'] = input_list.FuzzyWuzzy.apply(lambda x: x[1])
input_list['FuzzyWuzzy'] = input_list.FuzzyWuzzy.apply(lambda x: return_value(x[0],match_against_clean))

### tooks 8 mins to 800 names to compare
now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Finish comparisons')


########## Heuristic to know the truth ##############

def eval_match(input_str, levenshtein, RatcliffObershelp, FuzzyWuzzy,FuzzyWuzzy_score):
	if levenshtein == RatcliffObershelp == FuzzyWuzzy:
		return levenshtein
	elif FuzzyWuzzy_score > 94:
		return FuzzyWuzzy
	else:
		return compare_search(input_str, levenshtein, RatcliffObershelp, FuzzyWuzzy)
		# return 'none'

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Start Heuristic')

input_list['match'] = input_list.apply(lambda row: eval_match(row['supplier_name'],row['Levenshtein'],row['RatcliffObershelp'],row['FuzzyWuzzy'], row['FuzzyWuzzy_score']), axis=1)

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Finish')


'''
now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - RatcliffObershelp')

input_list['RatcliffObershelp'] = input_list.supplier_name.apply(lambda x: RatcliffObershelp(x,list(set(match_against.vendor_name))))

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Levenshtein')

input_list['Levenshtein'] = input_list.supplier_name.apply(lambda x: Levenshtein(x,list(set(match_against.vendor_name))))

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - FuzzyWuzzy')

input_list['FuzzyWuzzy'] = input_list.supplier_name.apply(lambda x: list(process.extractOne(x,list(set(match_against.vendor_name)))))

now = datetime.datetime.now()
print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - Finish')

'''
