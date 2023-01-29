import pandas as pd
from model.model import BellModel
import torch
from PIL import Image
from torch.utils.data import DataLoader
from BillDataset import BillDataset
import os

#given the # of days since 1970 and the amount, find the receipt name


## assuming the data input is three lists of the number of days and amount...
document_id = ['00034'] 
number_of_days = [17923]
amount = [37.1]
id_dict = {}
correct = 0

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
amount = out['Amount'].detach().cpu()[0]
number_of_days = out['Date'].detach().cpu()[0]


for ind, val in enumerate(number_of_days):
    id = None
    for i in range(len(dataframe.index)):
        if amount[ind] == dataframe['amount'][i] and number_of_days[ind] == dataframe['date'][i]:
            id = i
            break
    if id == None:
        for i in range(len(dataframe.index)):
            if number_of_days[ind] == dataframe['date'][i]: # the amount in the csv would be zero not the prediction
                id = i
                break
    if id == None:
        for i in range(len(dataframe.index)):
            if amount == dataframe['amount'][i]: # may not want to force it to be 0 .. could just search for unique amount
                id = i
                break
        
    # check to see if the documentid and image id match... 
    predict_doc_id = dataframe['documentid'][id]
    id_dict[document_id[ind]] = predict_doc_id # dictionary of values 
    
    if document_id[ind] == predict_doc_id :
        correct += 1   

#---- Calculating accuracy 
acc = correct/len(number_of_days)
print('The accuracy on the test set is:', acc)