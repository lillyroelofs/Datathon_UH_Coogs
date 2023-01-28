from datetime import date
from datetime import datetime
from email.utils import formatdate
import pandas as pd



dataframe = pd.read_csv("Users.csv")
date1 = date(1970,1,1)
count=0
all_days = []
for i in range(len(dataframe['date'])):
    date_str = dataframe['date'][i]
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
    dataframe['date'][i] = days
    all_days.append(days)
print(all_days)


    
dataframe.to_csv("Users_days_updated.csv")

print(count)