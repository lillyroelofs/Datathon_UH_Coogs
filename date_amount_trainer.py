from datetime import date
import enum
from model.model import BellModel
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from BillDataset import BillDataset
import os
from model.double_densenet import DoubleDenseNet

BATCH_SIZE = 4
EPOCHS = 10000

device = torch.device('cuda:0') 
model = DoubleDenseNet().to(device)

criterion = torch.nn.MSELoss()
optimizer1 = optim.SGD(model.Date_head.parameters(),lr=0.00001)
optimizer2 = optim.SGD(model.Amount_head.parameters(),lr=0.00001)

min_loss = 10000000000
min_val_loss = 10000000000
loss_list = []
val_loss_list = []

train_dataset = BillDataset(csv_file="train.csv",root_dir=os.getcwd(),transform=True)
val_dataset = BillDataset(csv_file="validation.csv",root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(train_dataset,batch_size=BATCH_SIZE,shuffle=True, pin_memory=True,drop_last=True)

validation_dataloader = DataLoader(val_dataset, batch_size=2,shuffle=True, pin_memory=True,drop_last=True)

def test_val_accuracy(model, dataloader):
    val_loss = 0
    samples = 0 
    with torch.no_grad():
        for batch, data in enumerate(dataloader):
            samples +=1
            img, gt = data
            out = model(img.to(device))
            #amount_date.to(device)
            amount = torch.squeeze(out["Amount"].float().to(device))
            out_date = torch.squeeze(out["Date"].float().to(device))
            amount_gt = gt[:,0].to(device).float()
            date_gt = gt[:,1].to(device).float()
            loss = torch.mean(torch.abs(out_date.float()-date_gt)) + torch.mean(torch.abs(amount.float() - amount_gt)) 
            val_loss = val_loss + loss
    return val_loss/samples

itr = 0 
for epoch in range(EPOCHS):
    print(f"epoch {epoch}")
    for batch, data in enumerate(train_dataloader):
        optimizer1.zero_grad()
        optimizer2.zero_grad()

        #print(f" batch {batch}")
        img, gt = data
        #print(f"img data  {img.shape}")
        #print(f"date and amount vector {amount_date.shape} ")
        out = model(img.to(device))
        #amount_date.to(device)
        amount = torch.squeeze(out["Amount"].float().to(device))
        out_date = torch.squeeze(out["Date"].float().to(device))
        amount_gt = gt[:,0].to(device).float()
        date_gt = gt[:,1].to(device).float()
        print(f"sample predictions: date {out_date[1]}, amount {amount[1]}")
        loss1 = torch.mean(torch.abs(out_date.float()-date_gt))
        loss2 = torch.mean(torch.abs(amount.float() - amount_gt)) 
        loss1.backward()
        optimizer1.step()
        loss2.backward()
        optimizer2.step()
        loss = loss1 + loss2
        loss_list.append(loss.detach().cpu())
        itr+=1
        print(f"itr: {itr}, Loss {loss}")
        if loss < min_loss:
            print(f"min_loss at itr: {itr}, Loss {loss}")
            min_loss = loss
            torch.save(model.state_dict(), "min_training_loss_model.pth")

    val_loss = test_val_accuracy(model, validation_dataloader)
    val_loss_list.append(val_loss.detach().cpu())
    if val_loss < min_val_loss:
        print(f"min validation loss at epoch: {epoch}, Loss {val_loss}")
        torch.save(model.state_dict(), "min_val_loss_model.pth")
        min_val_loss = val_loss
    
    plt.plot(loss_list)
    plt.savefig("train_loss_plot.png")
    plt.close()
    plt.plot(val_loss_list)
    plt.savefig("val_loss_plot.png")
    plt.close()


# #check save and load model
torch.save(model.state_dict(), "model.pth")
#model.load_state_dict(torch.load("model.pth"))
