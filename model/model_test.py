from transformers import ConvNextImageProcessor, ConvNextForImageClassification
import torch
from datasets import load_dataset

dataset = load_dataset("huggingface/cats-image")
image = dataset["test"]["image"][0]
#pil image

feature_extractor = ConvNextImageProcessor.from_pretrained("facebook/convnext-xlarge-384-22k-1k")
model = ConvNextForImageClassification.from_pretrained("facebook/convnext-xlarge-384-22k-1k")

inputs = feature_extractor(image, return_tensors="pt")
print(inputs["pixel_values"].shape)

with torch.no_grad():
    logits = model(**inputs).logits

# model predicts one of the 1000 ImageNet classes
predicted_label = logits.argmax(-1).item()
print(model.config.id2label[predicted_label]),