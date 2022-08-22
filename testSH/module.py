import numpy as np
import pandas as pd
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding


def create_dataloader(data_file_path, pretrained, pretrained_model_path):
    if pretrained == "kbalbert":
        MAX_LEN = 512
        tokenizer = AutoTokenizer.from_pretrained(pretrained_model_path)
        tokenizer.truncation_side = "left"

        inference_dataset = load_dataset("csv", data_files=data_file_path)["train"]
        inference_dataset = inference_dataset.map(lambda data: tokenizer(data["article"], padding="max_length", max_length=MAX_LEN, truncation=True),
                                                  remove_columns=["Unnamed: 0", "company", "title", "opinion", "firm", "date", "article"])
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

        inference_dataloader = torch.utils.data.DataLoader(
            inference_dataset,
            sampler = torch.utils.data.SequentialSampler(inference_dataset),
            batch_size = 1,
            collate_fn = data_collator,
        )
    else:
        if pretrained == "roberta-large":
            tokenizer_path = 'klue/roberta-large'
        else:
            tokenizer_path = 'monologg/kobert'
            
        MAX_LEN = 512
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        tokenizer.truncation_side = "left"

        inference_dataset = load_dataset("csv", data_files=data_file_path)["train"]
        inference_dataset = inference_dataset.map(lambda data: tokenizer(data["article"], padding="max_length", max_length=MAX_LEN, truncation=True),
                                                  remove_columns=["Unnamed: 0", "company", "title", "opinion", "firm", "date", "article"])
        data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
        inference_dataloader = torch.utils.data.DataLoader(inference_dataset, shuffle=False, batch_size=1, collate_fn=data_collator)
    
    return inference_dataloader

def soft_voting(probabilities):
    return np.mean(probabilities, axis=0, dtype=np.float64)    

def save_csv_file(data_file_path, save_file_path, probabilities):
    ensemble_prob = np.mean(probabilities, axis=0, dtype=np.float64)
    ensemble_pred = (ensemble_prob > 50).astype(np.int32)

    inference_dataframe = pd.read_csv(data_file_path)

    convert_pred = list(map(lambda x: "매수" if x == 1 else "매도", ensemble_pred))
    convert_prob = list(map(lambda x: np.round(x, 2) if x > 50 else np.round(100 - x, 2), ensemble_prob))

    inference_dataframe = inference_dataframe.drop(labels="Unnamed: 0", axis=1)
    inference_dataframe["predictions"] = convert_pred
    inference_dataframe["pred_rate"] = convert_prob
    inference_dataframe.to_csv(save_file_path, index=False)