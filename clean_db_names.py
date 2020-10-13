### quitar stops words & most frequent words from supplier names
import pickle
import pandas as pd
from nltk.corpus import stopwords
from collections import Counter

def clean_list(list_to_clean):
	with open('stopwords','rb') as f:
		stop_words = pickle.load(f)
	filtered_names = []

	for name in list_to_clean:
		filtered_words = [w for w in name.lower().split() if not w in stop_words]
		filtered_name = ' '.join(filtered_words).replace('.','').replace(',','').lower()
		filtered_names.append([name,filtered_name])
	j = pd.DataFrame(filtered_names, columns=['original_name', 'clean_name'])
	type(j)
	return j

def clean_word(word_to_clean):
	with open('stopwords','rb') as f:
		stop_words = pickle.load(f)
	filtered_words = [w for w in word_to_clean.lower().split() if not w in stop_words]
	filtered_word = ' '.join(filtered_words).replace('.','').replace(',','').lower()
	return filtered_word


''' with open(r'G:\My Drive\AA\Brands matching\gsuggestion_df', "rb") as f:
	db = pickle.load(f)

list_of_suppliers = list(set(db.vendor_name))

stop_words = set(stopwords.words('english'))

corpus_supplier_names = ' '.join(list_of_suppliers)
supplier_words = corpus_supplier_names.split()

# Pass the split_it list to instance of Counter class. 
Counter = Counter(supplier_words) 
  
# most_common() produces k frequently encountered 
# input values and their respective counts. 
# quité el elemento "Scientific" de la lista y agregé ",", "." y "GB"

most_occur = Counter.most_common(15)

for item in most_occur:
	stop_words.add(item[0])
'''