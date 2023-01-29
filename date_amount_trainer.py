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

train_dataset = BillDataset(csv_file="Users_days_updated.csv",root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(train_dataset,batch_size=BATCH_SIZE,shuffle=True, pin_memory=True, num_workers = 8)

for epoch in range(EPOCHS):
    for batch,data in enumerate(train_dataloader):
        print(f" batch {batch}")
        print(f"data {data}")
    # out = model(x)
    # amount = out["Amount"]
    # date = out["Date"]
    # loss = criterion(date,gt.to(device)) + criterion(amount,gt_amount.to(device)) 
    # loss.backward()
    # optimizer.step()
    # loss_list.append(loss.detach().cpu())
    # if loss < min_loss:
    #     print(f"itr: {i}, Loss {loss}, predicted date {date[0]}, predicted amount {amount[0]}")
    #     min_loss = loss

# plt.plot(loss_list)
# plt.savefig("loss_plot.png")
# plt.close()

# #check save and load model
# torch.save(model.state_dict(), "model.pth")
# model.load_state_dict(torch.load("model.pth"))
