import pandas as pd
import numpy as np
import os
import gc
import random
import datasets
from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split
from soynlp.normalizer import emoticon_normalize, only_text
import re

import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

import pytorch_lightning as pl
from pytorch_lightning.loggers import TensorBoardLogger
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
import torchmetrics

from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score

import transformers
from transformers import get_scheduler, AdamW, get_linear_schedule_with_warmup
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, AutoConfig
from transformers import PreTrainedTokenizerFast, GPT2ForSequenceClassification, GPT2Config
from datasets import load_dataset
from flash.core.optimizers import LAMB

from tqdm.notebook import tqdm, trange
import warnings
warnings.filterwarnings("ignore")

def set_seeds(seed=42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False # for faster training, but not deterministic

def tokenize(data):
  return tokenizer(data['article'], max_length=512, pad_to_max_length = True, truncation=True)

set_seeds()

path = '/content/drive/MyDrive/reviewdataset'
train = pd.read_csv(path+'/traindataset.csv')
train = train[['article', 'label']]

train_df, val_df = train_test_split(train, test_size = 0.1, shuffle=True, random_state=42, stratify=train['label'])
train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)

tokenizer = AutoTokenizer.from_pretrained('monologg/kobert')

train_dataset = Dataset.from_pandas(train_df)
val_dataset = Dataset.from_pandas(val_df)

train_dataset = train_dataset.map(tokenize, batched=True)
val_dataset = val_dataset.map(tokenize, batched=True)

train_dataset = train_dataset.remove_columns(['article'])
val_dataset = val_dataset.remove_columns(['article'])

train_dataset = train_dataset.rename_columns(
    {
        "label": "labels"
    }
)
val_dataset = val_dataset.rename_columns(
    {
        "label": "labels"
    }
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=2, collate_fn=data_collator)
valid_dataloader = DataLoader(val_dataset, shuffle=True, batch_size=2, collate_fn=data_collator)

config = AutoConfig.from_pretrained('nile/koBERT-finetuned-wholemasking20')
config.num_labels = 2
model = AutoModelForSequenceClassification.from_pretrained('nile/koBERT-finetuned-wholemasking20', config=config)
MODEL_NAME = "koBERT-DAPT"

num_epochs = 20
optimizer = AdamW(model.parameters(), lr=1e-5)
num_training_steps = num_epochs * len(train_dataloader)
lr_scheduler = get_scheduler(
    "linear",
    optimizer=optimizer,
    num_warmup_steps=num_training_steps*0.1,
    num_training_steps=num_training_steps,
)
criterion = nn.CrossEntropyLoss()

device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
model.to(device)
gc.collect()
torch.cuda.empty_cache()

# train & validation & save model
loss_log = []
acc_log = []
best_predict = []
for i in range(num_epochs):
    progress_bar = tqdm(enumerate(train_dataloader), total=len(train_dataloader), leave=True, position=0)
    model.train()
    for j, v in progress_bar:
        input_ids, attention_mask, labels = v['input_ids'].to(device), v['attention_mask'].to(device), v['labels'].to(
            device)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask)  # label을 안 넣어서 logits값만 출력
        output = outputs.logits  # The outputs object is a SequenceClassifierOutput
        loss = criterion(output, labels)
        loss.backward()
        optimizer.step()
        lr_scheduler.step()
        valid_perform = np.zeros(2)

    all_valid_predict_lst = []
    all_valid_labels_lst = []
    progress_bar = tqdm(enumerate(valid_dataloader), total=len(valid_dataloader), leave=True, position=0)
    model.eval()
    with torch.no_grad():
        for _, v in progress_bar:
            input_ids, attention_mask, valid_labels = v["input_ids"].to(device), v["attention_mask"].to(device), v[
                "labels"].to(device)
            valid_outputs = model(input_ids, attention_mask)
            valid_output = valid_outputs.logits
            valid_loss = criterion(valid_output, valid_labels)

            valid_predict = valid_output.argmax(dim=-1)
            valid_predict = valid_predict.detach().cpu().numpy()
            # valid_labels = valid_labels.argmax(dim=-1)
            valid_labels = valid_labels.detach().cpu().numpy()
            valid_acc = accuracy_score(valid_labels, valid_predict)
            valid_perform += np.array([valid_loss.item(), valid_acc])

            all_valid_predict_lst += list(valid_predict)
            all_valid_labels_lst += list(valid_labels)

        val_total_loss = valid_perform[0] / len(valid_dataloader)
        val_total_acc = valid_perform[1] / len(valid_dataloader)
        print(f">>>> Validation loss: {val_total_loss}, Acc: {val_total_acc}")
        loss_log.append(val_total_loss)
        acc_log.append(val_total_acc)
        if i > 5:
            if loss_log[i] < loss_log[i - 1] and loss_log[i] < loss_log[i - 2] and loss_log[i] < loss_log[i - 3]:
                torch.save(model.state_dict(), f"/content/drive/MyDrive/reviewdataset/koBERTtrain.pt")
                best_predict = all_valid_predict_lst
            if acc_log[i] <= acc_log[i - 1] and acc_log[i - 1] <= acc_log[i - 2] and acc_log[i - 2] <= acc_log[i - 3]:
                break