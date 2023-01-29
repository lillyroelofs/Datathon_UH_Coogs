import torch
import torch.nn as nn
import torch.nn.functional as F
import timm

class BellModel(torch.nn.Module):

    def __init__(self):
        super(BellModel, self).__init__()
        self.encoding_dimension = 21841
        self.Activation = torch.nn.ReLU()
        self.Feature_Extraction = timm.create_model('convnext_large_in22k', pretrained=True)
        
        #self.DropOut = F.dropout
        
        #layers for head 1, Amount prediction
        self.Amount_linear_1 = torch.nn.Linear(self.encoding_dimension,int(self.encoding_dimension/2))
        self.Amount_norm = nn.BatchNorm1d(int(self.encoding_dimension/2))
        self.Amount_linear_2 = torch.nn.Linear(int(self.encoding_dimension/2),1)
        self.Amount_head = torch.nn.Sequential(self.Amount_linear_1,self.Amount_norm,self.Activation, self.Amount_linear_2)#adjust based on sensitivity/response
        

        #layers for head 2, Date head
        self.Date_linear_1 = torch.nn.Linear(self.encoding_dimension,int(self.encoding_dimension/2))
        self.Date_norm = nn.BatchNorm1d(int(self.encoding_dimension/2))
        self.Date_linear_2 = torch.nn.Linear(int(self.encoding_dimension/2),1)
        self.Date_head = torch.nn.Sequential(self.Date_linear_1, self.Date_norm,self.Activation, self.Date_linear_2)#adjust based on sensitivity/response
        
        #layers for head 3, Name Head
        #max_number_of_character x 6
        #ToDo

    def forward(self,x):
        features = self.Feature_Extraction(x)
        #feed forward for Amount
        #print(features.shape)
        Amount = self.Amount_head(features)
        
        #feed forward for Date
        Date = self.Date_head(features)

        inference = {"Amount":Amount,"Date":Date}
        
        return inference
            

















