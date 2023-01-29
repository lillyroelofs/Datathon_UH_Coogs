from model.model import BellModel
import torch
import torch.optim as optim
import matplotlib.pyplot as plt
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


device = torch.device('cuda') 
model = BellModel().to(device)
BATCH_SIZE = 6
gt = torch.ones([BATCH_SIZE,1])*1234
print(gt[0])
gt_amount = torch.ones([BATCH_SIZE,1])*456.12

criterion = torch.nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)
x = torch.randn(BATCH_SIZE, 3, 256, 256).to(device)
#test if date head can generate ground truth
min_loss = 1000000
loss_list = []

for i in range(300):
    
    out = model(x)
    amount = out["Amount"]
    date = out["Date"]
    loss = criterion(date,gt.to(device)) + criterion(amount,gt_amount.to(device)) 
    loss.backward()
    optimizer.step()
    loss_list.append(loss.detach().cpu())
    if loss < min_loss:
        print(f"itr: {i}, Loss {loss}, predicted date {date[0]}, predicted amount {amount[0]}")
        min_loss = loss

plt.plot(loss_list)
plt.savefig("loss_plot.png")
plt.close()

#check save and load model
torch.save(model.state_dict(), "model.pth")
model.load_state_dict(torch.load("model.pth"))
loss_list = []
for i in range(300):
    
    out = model(x)
    amount = out["Amount"]
    date = out["Date"]
    loss = criterion(date,gt.to(device)) + criterion(amount,gt_amount.to(device)) 
    loss.backward()
    optimizer.step()
    loss_list.append(loss.detach().cpu())
    if loss < min_loss:
        print(f"itr: {i}, Loss {loss}, predicted date {date[0]}, predicted amount {amount[0]}")
        min_loss = loss

plt.plot(loss_list)
plt.savefig("loss_plot_after_loading.png")