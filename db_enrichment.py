import pandas as pd
import psycopg2
import time
import pickle
from pytrends.request import TrendReq


connection = psycopg2.connect(user = "valentina_ariel",
                              password = "ZpYYGld6bz6tetUi",
                              host = "reporting.zageno.com",
                              port = "31870",
                              database = "zageno")

cur = connection.cursor()

cur.execute("""SELECT DISTINCT
                    ven.name AS vendor_name
                FROM zageno_master.vendor_core_vendor AS ven
                ;""")
vendor_name_db = [r[0] for r in cur.fetchall()]

cur.close()

pytrend = TrendReq()

gsuggestion = pd.DataFrame()
t=0
for vendor_name in vendor_name_db:
	try:
		keywords = pytrend.suggestions(keyword=vendor_name)
	except:
		print('An error occurred on index:')
		print(vendor_name_db.index('Net32 Inc.'), vendor_name_db.index(vendor_name))
	if keywords:
		suggestions_i = pd.DataFrame(keywords)
		suggestions_i['vendor_name'] = vendor_name
	else:
		suggestions_i = pd.DataFrame()
		suggestions_i['vendor_name'] = [vendor_name]
	gsuggestion = pd.concat([gsuggestion,suggestions_i],axis=0, sort=False,ignore_index=True)

with open(r'G:\My Drive\AA\Brands matching\gsuggestion_df', "wb") as f:
    pickle.dump(gsuggestion, f)


input_list = pd.DataFrame()
match_list = pd.DataFrame()
comparison_output = pd.DataFrame()



		if t == 300:  
			print('too many errors.. abort')
			break
		else:
			now = datetime.datetime.now()
			t = t + 60
			print(now.day,'.',now.month,'.',now.year,' - ', now.hour, ':', now.minute, ':', now.second, ' - An error ocurred, sleep for {}s'.format(t))
			time.sleep(t)