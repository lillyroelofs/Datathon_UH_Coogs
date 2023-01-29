import torch
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
import torchvision
import torch
from PIL import Image
import os

class BillDataset(Dataset):
    """BILL dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        Args:
            csv_file (string): Path to the csv file with annotations.
            root_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        self.bill_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.img_size = 512
        self.transform = torchvision.transforms.Compose([torchvision.transforms.Resize((512,512)),torchvision.transforms.ToTensor()])

    def __len__(self):
        return len(self.bill_frame)

    def __getitem__(self, idx):

        img_name = os.path.join("img",self.bill_frame.iloc[idx, 1])
        img_name = img_name + '.jpg'
        #print(img_name)
        img = Image.open(img_name)

      

        user = self.bill_frame.iloc[idx, 3:5]
        user = np.array(user)
        user_num = np.array([user[0],user[1]])
        #print(user_num)
        #print(type(user_num[0]))
        details = user_num
        img=img.resize([512,512])
        #img.save("testing.jpg")
        img = self.transform(img)
        if img.shape[0] == 1:
            #print(f"{img_name} has only 1 channel")
            img = img * torch.ones((3,512,512))
        details = torch.from_numpy(details)
    
        return img, details

# train_dataset = FaceusermarksDataset(csv_file="Users_days_updated.csv",root_dir=os.getcwd(),transform=True)
# train_dataloader = DataLoader(train_dataset,batch_size=1,shuffle=True)

# img, details = next(iter(train_dataloader))
# print(img.shape)
# print(details.shape)
# # plt.imshow(train['image'], cmap="gray")
# # plt.show()
