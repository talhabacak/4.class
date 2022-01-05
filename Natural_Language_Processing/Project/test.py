# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 12:34:52 2021

@author: talha
"""


import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
import torch
from transformers import TrainingArguments, Trainer
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import EarlyStoppingCallback



class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels=None):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        if self.labels:
            item["labels"] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.encodings["input_ids"])



path_test = "test.csv"
model_path = "finetuned_BERT_epoch_2.model"

model_name = "dbmdz/bert-base-turkish-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
test_data = pd.read_csv(path_test)
X_test = list(test_data["Görüş"])
X_test_tokenized = tokenizer(X_test, padding=True, truncation=True, max_length=512)


test_dataset = Dataset(X_test_tokenized)


model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)
model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))


test_trainer = Trainer(model)

raw_pred, _, _ = test_trainer.predict(test_dataset)

y_pred = np.argmax(raw_pred, axis=1)

#print("\n"*50)

index=0;
for i in y_pred: 
    print(test_data["Görüş"][index], end=":\t")
    if i == 0:
        print("Olumsuz")
    else:
        print("Olumlu")
    index += 1
    
    