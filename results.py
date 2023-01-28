import pandas as pd

#given the # of days since 1970 and the amount, find the receipt name




number_of_days = 17923

amount = 37.1

dataframe = pd.read_csv("Users_days_updated.csv")


id = None
for i in range(len(dataframe.index)):
    if amount == dataframe['amount'][i] and number_of_days == dataframe['date'][i]:
        id = i
        break
if id == None:
    for i in range(len(dataframe.index)):
        if number_of_days == dataframe['date'][i] and amount == 0:
            id = i
            break
if id == None:
    for i in range(len(dataframe.index)):
        if amount == dataframe['amount'][i] and number_of_days == 0:
            id = i
            break
id = None
for i in range(len(dataframe.index)):
    if amount == dataframe['amount'][i] or number_of_days == dataframe['date'][i]:
        id = i
        break

print('The receipt id is',dataframe['documentid'][id])
