import pandas as pd
import json
import sys

#read arguments
if len(sys.argv) < 3: print('input and output file not found');sys.exit(0)
json_file=sys.argv[1]
output_file=sys.argv[2]

# load data using Python JSON module
with open(json_file,'r') as f:
   data = json.loads(f.read())

#preparing data
df_header = pd.json_normalize(data, record_path=['items','item'])[['id','type']]
df_batter = pd.json_normalize(data, record_path=['items','item','batters','batter'], meta=[['items','item','id']] )[['type','items.item.id']]
df_topping = pd.json_normalize(data, record_path=['items','item','topping'] , meta=[['items','item','id']])[['type','items.item.id']]

df_batter.rename(columns={'type':'Batter','items.item.id':'header_id'}, inplace=True)
df_topping.rename(columns={'type':'Topping','items.item.id':'header_id'}, inplace=True)

df_merge=df_header.merge(df_batter, left_on='id', right_on='header_id').merge(df_topping, left_on='id', right_on='header_id')[['id','type','Batter','Topping']]
df_merge.sort_values(by='id', inplace=True, ascending=True)


#convert to html
result = df_merge.to_html(index=False)

# write html to file
text_file = open(output_file, "w")
text_file.write(result)
text_file.close()