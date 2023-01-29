import pandas as pd
from model.model import BellModel
import torch
from PIL import Image
from torch.utils.data import DataLoader
from BillDataset import BillDataset
import os
#given the # of days since 1970 and the amount, find the receipt name


device = torch.device('cuda') 
model = BellModel().to(device)
model.load_state_dict(torch.load("min_training_loss_model.pth"))

val_dataset = BillDataset(csv_file="validation.csv",root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(val_dataset,batch_size=2,shuffle=False, pin_memory=True,drop_last=True)
for batch, data in enumerate(train_dataloader):

    #print(f" batch {batch}")
    img, gt = data
    #print(f"img data  {img.shape}")
    #print(f"date and amount vector {amount_date.shape} ")
    out = model(img.to(device))
dataframe = pd.read_csv("test_transactions.csv")
amount = out['Amount'].detach().cpu()[0][0]
number_of_days = out['Date'].detach().cpu()[0][0]

print(amount)
print(number_of_days)
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


if id is None:
    print("No transaction found")
else:
    print('The receipt id is',dataframe['documentid'][id])
