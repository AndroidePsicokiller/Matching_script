import re
import time
import difflib
import datetime
import textdistance
import pandas as pd
from googlesearch import search

def compare_search(input_str, levenshtein, RatcliffObershelp, FuzzyWuzzy):
	pat = re.compile(r'(http[s]?://)(.+?)(/)')
	compare_list_search = {}
	best_match = ['None',0.0]
	try:
		input_str_search = search(input_str)
		# input_list_search = [pat.search(x).group(2) for x in input_str_search]
		time.sleep(14)

		levenshtein_search = search(levenshtein)
		compare_list_search['Levenshtein'] = levenshtein_search # [pat.search(x).group(2) for x in levenshtein_search]
		time.sleep(14)

		RatcliffObershelp_search = search(RatcliffObershelp)
		compare_list_search['RatcliffObershelp'] = RatcliffObershelp_search # [pat.search(x).group(2) for x in RatcliffObershelp_search]
		time.sleep(14)

		FuzzyWuzzy_search = search(FuzzyWuzzy)
		compare_list_search['FuzzyWuzzy'] = FuzzyWuzzy_search # [pat.search(x).group(2) for x in FuzzyWuzzy_search]
		time.sleep(14)

		for key in compare_list_search.keys():
			# jdistance = textdistance.jaccard(input_list_search,compare_list_search[key])
			sm = difflib.SequenceMatcher(None,input_str_search,compare_list_search[key])
			# if jdistance > best_match[1]:
			# 	best_match = [key,jdistance]
			if sm.ratio() > best_match[1]:
				best_match = [key,sm.ratio()]
		
		return best_match
	except:
		now = datetime.datetime.now()
		print('error ocurred - sleep 1 min', now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second)
		time.sleep(60)
		return 'error'