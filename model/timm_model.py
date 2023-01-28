import timm 
import torch


model = timm.create_model('convnext_xlarge_in22k')
x = torch.randn(1, 3, 224, 224)
print(model(x))