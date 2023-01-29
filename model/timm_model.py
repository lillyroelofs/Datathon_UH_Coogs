import timm 
import torch


model = timm.create_model('convnext_large_in22k')
x = torch.randn(1, 3, 224, 224)
out = model(x)
print(out)
for temp in out:
    print(temp.shape)