import pandas as pd

df = pd.read_json(r'reviews.json', encoding='utf-8')
df['hours'].astype('float')

df.to_csv(r'reviews.csv', index = None, encoding='utf-8-sig', sep = ';' , float_format='%.1f' )
