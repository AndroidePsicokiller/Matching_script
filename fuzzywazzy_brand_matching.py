from fuzzywuzzy import process
import pandas as pd

brands_db = pd.read_excel(r'G:\My Drive\AA\Brands matching\brand_db.xlsx')
brands_to_match_pd = pd.read_csv(r'G:\My Drive\Catalogs Local\Daigger\brand_normalization_daigger.csv')
brands_to_match = list(brands_to_match_pd['Brand Name'])
brands_name = list(brands_db['brand_name'])
output_match = pd.DataFrame()
aux = pd.DataFrame()

for brand in brands_to_match:
	fuzzy_match = process.extractOne(brand,brands_name)
	aux = brands_db.loc[brands_db['brand_name'] == fuzzy_match[0]]
	aux['Score'] = fuzzy_match[1]
	aux['Supplier brand'] = brand
	output_match = pd.concat([output_match,aux],axis=0, sort=False)
	# output_match = pd.concat([output_match,brands_db.loc[brands_db['brand_name'] == fuzzy_match[0]]],axis=0, sort=False)

# output_match['Supplier brands'] = brands_to_match