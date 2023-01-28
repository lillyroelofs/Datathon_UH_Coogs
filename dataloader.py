from __future__ import print_function, division
import os
from tkinter import image_names
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import cv2
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
from torchvision import transforms, utils
import torch



#document id is img name
# bill_frame = pd.read_csv('Users.csv')

# n = 306
# img_name = bill_frame.iloc[n, 0]
# img_name = img_name + '.jpg'

# image = io.imread(img_name)
# user_details = bill_frame.iloc[n, 1:]
# user = np.asarray(user_details)
# #user = user.astype('float').reshape(-1, 2)
# details = user[1:4]
# sample = {'image': image, 'user_details': details}

# vectorizer = CountVectorizer()
# sentence_vectors = vectorizer.fit_transform([details[2]])
# print(details[2])
# print(sentence_vectors.toarray())



class FaceusermarksDataset(Dataset):
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
        self.transform = transform

    def __len__(self):
        return len(self.bill_frame)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = os.path.join(self.root_dir,
                                self.bill_frame.iloc[idx, 0])
        img_name = img_name + '.jpg'
        image = io.imread(img_name)
        user = self.bill_frame.iloc[idx, 1:]
        user = np.array([user])
        details = user[1:4]
        sample = {'image': image, 'user_details': details}

        if self.transform:
            sample['image'] = cv2.resize(sample['image'],dsize=(100,100),interpolation=cv2.INTER_CUBIC)
        print(sample['user_details'])
        return sample

train_dataset = FaceusermarksDataset(csv_file="Users.csv",root_dir=os.getcwd(),transform=True)
train_dataloader = DataLoader(train_dataset,batch_size=32,shuffle=True)


train = next(iter(train_dataloader))
plt.imshow(train['image'], cmap="gray")
plt.show()