### Importing and cleaning the csv data 

## import libraries 
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime
from email.utils import formatdate
from sklearn.utils import shuffle
import math

## initialize 
filename = 'Users.csv' # test_transactions.csv
final_filename = 'train.csv' # test.csv
training = 1 # used to set whether we are looking at the training or testing set. if we are doing training, need to randomize and split 
extra_name = 'validation.csv'

## import data
user_data = pd.read_csv(filename) 

## assumptions: document id and user id are correct. 
# errors associated with...
    # amount - additional decimals places, empty field, decimal placed in the wrong location, completely wrong amount, comma instead of decimal?
    # date - different formats, incorrect date/extra numbers
    # vendor name - misspelled

## ridding the dataframe of empty/NaN cells 
user_data = user_data.replace([np.NaN], 0)

## cleaning the amount column
# rounding all incorrect decimal places to 2
for ind, val in enumerate(user_data['amount']):
    if len(str(val).split(".")[1]) > 2:
        user_data['amount'] = user_data['amount'].replace([val], round(val, 2)) # this will change any of the cells with this unique value to the rounded one (which is the goal anyways so that's fine)

## standardizing the name
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


## fixing the date -- GEORGE
date1 = date(1970,1,1)
count=0
todays_date = datetime.now().date()
for i in range(len(user_data['date'])):
    date_str = user_data['date'][i]
    if '-' in date_str:
        first,last = date_str.split('-',1)
        if(int(first)>200):
            format_data = '%Y-%m-%d'
        else:
            format_data = '%d-%m-%Y'
    if '/' in date_str:
        first,last = date_str.split('/',1)
        if(int(first)>200):
            format_data = '%Y/%m/%d'
        else:
            format_data = '%m/%d/%Y'
    try:
        date2 = datetime.strptime(date_str,format_data)
        date2 = date2.date()
        days = (date2-date1).days
    except:
        count=count+1
        days=0

    if((date2-todays_date).days>0):
        days=0
    if((date2-date1).days<0):
        days=0
    user_data['date'][i] = days

## for training, randomize and split. for testing, save to csv. 
if training == 1:
    user_data = shuffle(user_data, random_state = 3) # shuffle
    split_point = math.ceil(len(user_data)*0.8)  # split
    train_data = user_data.iloc[:split_point]
    valid_data = user_data.iloc[split_point:] # no overlap since python cuts off before the last number 
    train_data.to_csv(final_filename)
    valid_data.to_csv(extra_name)
else: 
    user_data.to_csv(final_filename)
