### Importing and cleaning the csv data 

## import libraries 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

## import data
user_data = pd.read_csv('../Users.csv')

## assumptions: document id and user id are correct. 
# errors associated with...
    # amount - additional decimals places, empty field, decimal placed in the wrong location, completely wrong amount, comma instead of decimal?
    # date - different formats 

# print(str(user_data['amount'][115]))
# print(len(str(user_data['amount'][115]).split(".")[1])) # determines the number of decimals places 

## cleaning the amount 
# ridding of an empty/NaN cells 
user_data = user_data.replace([np.NaN], 0)
# rounding all incorrect decimal places to 2
for ind, val in enumerate(user_data['amount']):
    if len(str(val).split(".")[1]) > 2:
        user_data['amount'] = user_data['amount'].replace([val], round(val, 2)) # this will change any of the cells with this unique value to the rounded one (which is the goal anyways so that's fine)


## name
# separate the series, change it, remove the old, and insert it
# constants
bad_chars = set('''-()'&?:!"\/;.,0123456789 ''')
names = user_data['vendor_name']
# remove characters from the names
for indi, vali in enumerate(names):
    names[indi] = ''.join( c for c in vali if  c not in bad_chars)  
# determine the longest string
largest_num = max(names, key=len) ## longest string 
# remove the old series
user_data = user_data.drop('vendor_name', axis=1)
# replace the series in the dataframe
user_data.insert(4, 'vendor_names', names)


''' 
# for ind, val in enumerate(user_data['vendor_name']):
# insert column with user_data.insert(column_pos, key_name_name, value)
new_row = pd.Series(list(np.arange(1, 500)))
user_data.insert(1, 'bonus1', new_row)
print(user_data)
user_data = user_data.drop('bonus1', axis=1)
print(user_data)

'''        

'''
for i in user_data['amount']:
    if len(str(i).split(".")[1]) > 2:
        print(i)
        print(round(user_data['amount'][i], 2))
'''