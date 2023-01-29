import torch
import torch.nn as nn
import torch.nn.functional as F
import timm

class DoubleDenseNet(torch.nn.Module):

    def __init__(self):
        super(DoubleDenseNet, self).__init__()
        #self.encoding_dimension = 21841 # for convnext

        self.Date_head = timm.create_model('densenet264', num_classes=1)
        self.Amount_head = timm.create_model('densenet264', num_classes=1)
        #layers for head 3, Name Head
        #max_number_of_character x 6
        #ToDo

    def forward(self,x):
        #features = self.Feature_Extraction(x)
        #feed forward for Amount
        #print(features.shape)
        Amount = F.relu(torch.abs(self.Amount_head(x)*10))
        
        #feed forward for Date
        Date = F.relu(self.Date_head(x)*100) + 17000

        inference = {"Amount":Amount,"Date":Date}
        
        return inference
            

















