import pandas as pd
import torch
from datasets import load_dataset
from transformers import AutoTokenizer, DataCollatorWithPadding
from sklearn.model_selection import train_test_split, StratifiedKFold


def load_dataframe(data_path, data_file):
    data_frame_list = list()
    
    for file_name in data_file:
        data_frame_list.append(pd.read_csv(data_path + file_name))
        
    all_data = pd.concat(data_frame_list)
    all_data.sample(frac=1).reset_index(drop=True)
    
    return all_data

def data_split(all_data, data_path, fold_length):
    train_data, test_data = train_test_split(all_data, test_size=0.2, random_state=42, stratify=all_data[["label"]])

    test_data["labels"] = test_data["label"]
    test_data = test_data.drop(labels=["filename", "length", "label"], axis=1)

    X = train_data.drop(labels=["filename", "length", "label"], axis=1)
    y = train_data["label"]

    skf = StratifiedKFold(n_splits=fold_length, shuffle=True, random_state=42)
    fold_dataframe = list()

    for fold_number, (train, valid) in enumerate(skf.split(X, y), 1):
        X_train, X_valid = X.iloc[train], X.iloc[valid]
        y_train, y_valid = y.iloc[train], y.iloc[valid]

        fold_train = X_train.loc[:]
        fold_train["labels"] = y_train

        fold_valid = X_valid.loc[:]
        fold_valid["labels"] = y_valid

        fold_train.to_csv(data_path + f"train_data_fold{fold_number}.csv", index=False)
        fold_valid.to_csv(data_path + f"valid_data_fold{fold_number}.csv", index=False)

    test_data.to_csv(data_path + "test_data.csv", index=False)
    
def tokenized_fn(data, tokenizer, max_len):
    outputs = tokenizer(data["article"], padding="max_length", max_length=max_len, truncation=True)
    outputs["labels"] = data["labels"]
    
    return outputs

def load_csv_to_dataset(model_path, pretrained_model, fold_length):
    tokenizer = AutoTokenizer.from_pretrained(model_path + pretrained_model)
    tokenizer.truncation_side = "left"
    
    MAX_LEN = 512

    dataset_list = list()
    for fold_number in range(1, fold_length+1):
        train_dataset = load_dataset("csv", data_files=f"./data/train_data_fold{fold_number}.csv")["train"]
        valid_dataset = load_dataset("csv", data_files=f"./data/valid_data_fold{fold_number}.csv")["train"]

        train_dataset = train_dataset.map(tokenized_fn, remove_columns=["article"], fn_kwargs={"tokenizer": tokenizer, "max_len": MAX_LEN})
        valid_dataset = valid_dataset.map(tokenized_fn, remove_columns=["article"], fn_kwargs={"tokenizer": tokenizer, "max_len": MAX_LEN})

        dataset_list.append([train_dataset, valid_dataset])

    test_dataset = load_dataset("csv", data_files=f"./data/test_data.csv")["train"]
    test_dataset = test_dataset.map(tokenized_fn, remove_columns=["article"], fn_kwargs={"tokenizer": tokenizer, "max_len": MAX_LEN})
    
    return dataset_list, test_dataset

def create_train_dataloader(dataset_list, test_dataset, model_path, pretrained_model, batch_size):
    tokenizer = AutoTokenizer.from_pretrained(model_path + pretrained_model)
    tokenizer.truncation_side = "left"
    
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    dataloader_list = list()
    for train_fold, valid_fold in dataset_list:
        train_dataloader = torch.utils.data.DataLoader(
            train_fold,
            sampler = torch.utils.data.RandomSampler(train_fold),
            batch_size = batch_size,
            collate_fn = data_collator,
        )

        validation_dataloader = torch.utils.data.DataLoader(
            valid_fold,
            sampler = torch.utils.data.SequentialSampler(valid_fold),
            batch_size = batch_size,
            collate_fn = data_collator,
        )

        dataloader_list.append([train_dataloader, validation_dataloader])

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        sampler = torch.utils.data.SequentialSampler(test_dataset),
        batch_size = batch_size,
        collate_fn = data_collator,
    )
    
    return dataloader_list, test_dataloader

def create_inference_dataloader(data_file_path, pretrained, pretrained_model_path):
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