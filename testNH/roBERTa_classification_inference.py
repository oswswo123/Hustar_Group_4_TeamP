import pandas as pd
import numpy as np
import os
import gc
import random
import datasets
from datasets import load_dataset, Dataset
from sklearn.model_selection import train_test_split

import torch
import torch.nn as nn
from torch.nn import CrossEntropyLoss
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from sklearn.metrics import accuracy_score

import transformers
from transformers import get_scheduler, AdamW, get_linear_schedule_with_warmup
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DataCollatorWithPadding, AutoConfig
from datasets import load_dataset

from tqdm.notebook import tqdm
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
    tokenizer = AutoTokenizer.from_pretrained('klue/roberta-large')
    return tokenizer(data['article'], max_length=512, pad_to_max_length = True, truncation=True)

def loaddataset(file):
    tokenizer = AutoTokenizer.from_pretrained('klue/roberta-large')
    test_dataset = load_dataset('csv', data_files=file)
    test_dataset = test_dataset.map(tokenize, batched=True)
    test_dataset['train'] = test_dataset['train'].remove_columns(
        ['Unnamed: 0', 'company', 'title', 'article', 'opinion', 'firm', 'date'])
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    eval_dataloader = DataLoader(test_dataset['train'], shuffle=False, batch_size=1, collate_fn=data_collator)
    return eval_dataloader

def loadmodel(model):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    config = AutoConfig.from_pretrained('nile/roBERTa-finetuned-wholemasking20')
    config.num_labels = 2
    load_model = AutoModelForSequenceClassification.from_pretrained('nile/roBERTa-finetuned-wholemasking20',
                                                                    config=config)
    load_model.to(device)
    load_model.load_state_dict(torch.load(model))
    return load_model

def inference(load_model, eval_dataloader, file):
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    load_model.eval()

    probabilities = list()
    predictions = list()

    for step, batch in enumerate(tqdm(eval_dataloader, desc="inference", mininterval=0.1)):
        batch_input_ids = batch["input_ids"].to(device)
        batch_attention_mask = batch["attention_mask"].to(device)

        with torch.no_grad():
            outputs = load_model(
                input_ids=batch_input_ids,
                attention_mask=batch_attention_mask,
            )

            prob = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predict = torch.argmax(prob, axis=1)
            prob = np.trunc(np.max(prob.detach().cpu().numpy(), axis=1) * 100)
            predict = predict.detach().cpu().numpy()

            probabilities.append(prob[0])
            predictions.append(predict[0])

    data = pd.read_csv(file)
    convert_predictions = list(map(lambda x: "매수" if x == 1 else "매도", predictions))
    inference_dataframe = data.drop(labels="Unnamed: 0", axis=1)
    inference_dataframe["predictions"] = convert_predictions
    inference_dataframe["pred_rate"] = probabilities
    inference_dataframe.to_csv("roBERTainferenced.csv", index=False)



set_seeds()
file = "inferencedatasetprocessed.csv"
eval_dataloader = loaddataset(file)
model = "roBERTatrain.pt"
load_model = loadmodel(model)

gc.collect()
torch.cuda.empty_cache()

inference(load_model, eval_dataloader, file)


