from datetime import date
from model.model import BellModel
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from BillDataset import BillDataset
import os

BATCH_SIZE = 6
EPOCHS = 100

device = torch.device('cuda') 
model = BellModel().to(device)

criterion = torch.nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

min_loss = 1000000
loss_list = []

train_dataset = BillDataset(csv_file="Updated_Users.csv",root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(train_dataset,batch_size=BATCH_SIZE,shuffle=True, pin_memory=True,drop_last=True)
itr = 0 
for epoch in range(EPOCHS):
    print(f"epoch {epoch}")
    for batch, data in enumerate(train_dataloader):

        #print(f" batch {batch}")
        img, gt = data
        #print(f"img data  {img.shape}")
        #print(f"date and amount vector {amount_date.shape} ")
        out = model(img.to(device))
        #amount_date.to(device)
        amount = out["Amount"].float().to(device)
        out_date = out["Date"].float().to(device)
        loss = criterion(out_date.float(),gt[:,1].to(device).float()) + criterion(amount.float(),gt[:,0].to(device).float()) 
        loss.backward()
        optimizer.step()
        loss_list.append(loss.detach().cpu())
        itr+=1
        print(f"itr: {itr}, Loss {loss}")
        if loss < min_loss:
            print(f"min_loss at itr: {itr}, Loss {loss}")
            min_loss = loss
            torch.save(model.state_dict(), "min_loss_model_itr.pth")


# plt.plot(loss_list)
# plt.savefig("loss_plot.png")
# plt.close()

# #check save and load model
torch.save(model.state_dict(), "model.pth")
#model.load_state_dict(torch.load("model.pth"))
