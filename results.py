import pandas as pd
#from model.model import BellModel
import torch
from PIL import Image
from torch.utils.data import DataLoader
from BillDataset import BillDataset
import os
from model.double_densenet import DoubleDenseNet as BellModel
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

filename = "test.csv"
test_dataset = BillDataset(csv_file=filename,root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(test_dataset,batch_size=2,shuffle=False, pin_memory=True,drop_last=True)

dataframe = pd.read_csv(filename)
document_ids = dataframe['documentid']
total_num=0
for batch, data in enumerate(train_dataloader):
    img, gt = data
    #print(gt)
    #print(f"img data  {img.shape}")
    #print(f"date and amount vector {amount_date.shape} ")
    out = model(img.to(device))
    
    amount = out['Amount'].detach().cpu()
    number_of_days = out['Date'].detach().cpu()
   # for i in range(len(gt)):
    avg_amount=0
    avg_days=0
    for x in range(len(gt)):
        if x==0:
            avg_amount=(amount[x][0] -  gt[x][0])
        if x==1:
            avg_days = number_of_days[x][0] - gt[x][0]
        total_num=total_num+1

print(avg_amount/total_num)
print(avg_days/total_num)
    # for j in range(len(amount)):
    #     id = None
    #     for i in range(len(dataframe.index)):
    #         if amount[j][0] == dataframe['amount'][i] and number_of_days[j][0] == dataframe['date'][i]:
    #             id = i
    #             break
    #     if id == None:
    #         for i in range(len(dataframe.index)):
    #             if number_of_days[j][0]== dataframe['date'][i]: # the amount in the csv would be zero not the prediction
    #                 id = i
    #                 break
    #     if id == None:
    #         for i in range(len(dataframe.index)):
    #             if amount[j][0]== dataframe['amount'][i]: # may not want to force it to be 0 .. could just search for unique amount
    #                 id = i
    #                 break
            
    #     # check to see if the documentid and image id match... 
    #    # predict_doc_id = dataframe['documentid'][id]
    #     #id_dict[document_id[ind]] = predict_doc_id # dictionary of values 
        
    #   #  if document_id[ind] == predict_doc_id :
    #    #     correct += 1   
    #     if id != None:
    #         correct+=1


#---- Calculating accuracy 
# acc = correct/len(dataframe.index)
# print('The accuracy on the test set is:', acc)