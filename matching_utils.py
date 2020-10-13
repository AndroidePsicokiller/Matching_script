import textdistance


def RatcliffObershelp(str1, list_to_match):
	best_match = ['',0]
	str_comparison = [[x,textdistance.ratcliff_obershelp(str1,x)] for x in list_to_match]
	for item in str_comparison:
		if item[1] > best_match[1]:
			best_match = item

	return best_match

def Levenshtein(str1, list_to_match):
	best_match = ['',10000000]
	str_comparison = [[x,textdistance.levenshtein(str1,x)] for x in list_to_match]
	for item in str_comparison:
		if item[1] < best_match[1]:
			best_match = item

	return best_match

def edit_based(list_to_match, str1,function):
	best_match = ['',10000000]
	str_comparison = [[x,function(str1,x)] for x in list_to_match]
	for item in str_comparison:
		if item[1] < best_match[1]:
			best_match = item
	return best_match

def token_based(str1, list_to_match, fuction):
	best_match = ['',0]
	str_comparison = [[x,fuction(str1,x)] for x in list_to_match]
	for item in str_comparison:
		if item[1] > best_match[1]:
			best_match = item
