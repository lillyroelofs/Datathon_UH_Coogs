# Comparing vendors


## load libraries 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import textdistance 


## import data
og_filename = pd.read_csv('test_transactions.csv')
filename = 'test.csv' # test data after we removed characters from the names
user_data = pd.read_csv(filename)
names = list(user_data["vendor_names"]) # pull vendor information 
all_names = {}
room_for_error = 6


## loop
while len(names) > 0:
    chosen_val = names[0]
    all_names[chosen_val] = [chosen_val] # the number of entries in the dictionary (i.e. length of the list) corresponds to the number of entries in list 
    names.pop(0)
    for ind, val in enumerate(names):
        dist = textdistance.damerau_levenshtein(chosen_val, val)
        if dist <= room_for_error:
            all_names[chosen_val] += [val]
            names.pop(ind)

largest = {}
for key in all_names:
    if len(all_names[key]) > 5:
        largest[key] = len(all_names[key])
    # print('The vendor name (or a variation of it) is {} and the number of exact/similar names are: {}'.format(key, len(all_names[key])))

## compare and display 
index = []
for n in largest:
    for ind, row in user_data["vendor_names"]:
        if n == row:
            index += ind
            
act_names = [] 
for those in index:
    real_name = og_filename.iloc[those, 4]
    act_names += real_name 
    






