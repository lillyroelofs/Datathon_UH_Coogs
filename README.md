## Datathon_UH_Coogs

This project is a submission to the 2023 Rice Datathon from George Bittar, Subin Varghese, Lilly Roelofs. The competition project was hosted by Bill.com, and the goal was to "create a model that assigns each receipt to its corresponding user entry in Users.csv/test_transcations.csv by only using the information from the image and OCR data."

## General approach: 

Our motivation for the problem was to avoid using the OCR data completely by training a neural network to predict the receipt amount and date from the receipt image. We found that the date formatting was heterogeneous, so we calculated the number of days since 1/1/1970 and used that to train the network. From here, we used two densenet264 neural network models (one for the amount, the other for the date) to train the network. Afterwards, we took the output predictions per image and searched for them in the test_transactions.csv file. 

## Important links: 

Minimum Training Loss Model: https://drive.google.com/file/d/1jxDidzaPycfYZ2N60g6eFXEDZMEIKt_o/view?usp=sharing

Minimum Val Loss Model: https://drive.google.com/file/d/1yqSXq6eBHzuPrQZwUpKu3qOYefXumUnJ/view?usp=sharing 

Updated Presentation: https://docs.google.com/presentation/d/1QCEtkUO2A1qZk1i285-ZQdpGUbs9gptCNNG0ddf7P08/edit?usp=sharing 

Devpost Submission: https://devpost.com/software/gsl#updates 

## Test set performance:

Average difference between predicted and ground truths values:

Amount: $0.1394

Date: 136.91 Days






