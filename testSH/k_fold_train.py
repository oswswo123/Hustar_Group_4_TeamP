import sys, os
import json
import torch
import numpy as np
import pandas as pd
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding
from datasets import load_dataset
from sklearn.model_selection import train_test_split, StratifiedKFold
from datasets import load_dataset
from transformers import DataCollatorWithPadding
import random
from itertools import repeat
from tqdm import tqdm

sys.path.append(os.path.dirname(__file__))
import model


def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

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

def csv_load_to_dataset(model_path, pretrained_model, fold_length):
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

def create_dataloader(dataset_list, test_dataset, model_path, pretrained_model, batch_size):
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

def set_seed(seed_val):
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)
    
def train(dataloader_list, test_dataloader, model_path, pretrained_model, save_model, device, seed_val, epochs, fold_length):
    pretrained = AutoModel.from_pretrained(model_path + pretrained_model) 

    train_model = model.AInalyst(pretrained_model=pretrained)
    train_model.to(device)
    train_model = torch.nn.DataParallel(train_model)
    isParallel = True
    optimizer = torch.optim.AdamW(train_model.parameters(), lr=1e-5)

    set_seed(seed_val)

    for epoch in range(epochs):
        print(f"============ Epoch {epoch+1}/{epochs} ============")
        print("Training...")

        for fold_number, (train_dataloader, validation_dataloader) in enumerate(dataloader_list, 1):
            print(f"===== Epoch {epoch+1}/{epochs} - Fold {fold_number}/{fold_length} =====")
            total_train_loss = 0
            train_model.train()

            for step, batch in enumerate(train_dataloader):
                batch_input_ids = batch["input_ids"].to(device)
                batch_attention_mask = batch["attention_mask"].to(device)
                batch_labels = batch["labels"].to(device)

                train_model.zero_grad()

                logits, loss = train_model(
                    input_ids = batch_input_ids,
                    attention_mask = batch_attention_mask,
                    labels = batch_labels,
                )

                if isParallel:
                    loss = loss.mean()

                total_train_loss += loss.item()
                loss.backward()
                optimizer.step()

            avg_train_loss = total_train_loss / len(train_dataloader)
            print()
            print(" Average training loss: {0:.5f}".format(avg_train_loss))

            # Validation
            print()
            print("Running Validation...")

            train_model.eval()
            total_eval_accuracy = 0
            total_eval_loss = 0
            nb_eval_steps = 0

            for step, batch in enumerate(validation_dataloader):
                batch_input_ids = batch["input_ids"].to(device)
                batch_attention_mask = batch["attention_mask"].to(device)
                batch_labels = batch["labels"].to(device)

                with torch.no_grad():
                    logits, loss = train_model(
                        input_ids = batch_input_ids,
                        attention_mask = batch_attention_mask,
                        labels = batch_labels,
                    )

                    if isParallel:
                        loss = loss.mean()

                    total_eval_loss += loss.item()
                    logits = logits.detach().cpu().numpy()
                    label_ids = batch_labels.to("cpu").numpy()
                    total_eval_accuracy += flat_accuracy(logits, label_ids)

            avg_val_accuracy = total_eval_accuracy / len(validation_dataloader)
            print()
            print(" Valid Accuracy: {0:.5f}".format(avg_val_accuracy))

        # Test
        print(f"===== Epoch {epoch+1}/{epochs} - Test =====")
        print()
        print("Running Test...")

        train_model.eval()
        total_test_accuracy = 0
        total_test_loss = 0
        nb_test_steps = 0

        for step, batch in enumerate(test_dataloader):
            batch_input_ids = batch["input_ids"].to(device)
            batch_attention_mask = batch["attention_mask"].to(device)
            batch_labels = batch["labels"].to(device)

            with torch.no_grad():
                logits, loss = train_model(
                    input_ids = batch_input_ids,
                    attention_mask = batch_attention_mask,
                    labels = batch_labels,
                )

                if isParallel:
                    loss = loss.mean()

                total_test_loss += loss.item()
                logits = logits.detach().cpu().numpy()
                label_ids = batch_labels.to("cpu").numpy()
                total_test_accuracy += flat_accuracy(logits, label_ids)

        avg_test_accuracy = total_test_accuracy / len(test_dataloader)
        print()
        print(" Test Accuracy: {0:.5f}".format(avg_test_accuracy))
        print()    

def main():
    json_file = open("./train_config.json", encoding="utf-8")
    key_dict = json.loads(json_file.read())
    
    fold_length = key_dict["fold_length"]
    batch = key_dict["batch"]
    seed_val = key_dict["seed_val"]
    epochs = key_dict["epochs"]
    data_path = key_dict["data_path"]
    data_file = key_dict["data_file"]
    model_path = key_dict["model_path"]
    pretrained_model = key_dict["pretrained_model"]
    save_model = key_dict["save_model"]
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    all_data = load_dataframe(data_path, data_file)
    data_split(all_data, data_path, fold_length)   
    
    dataset_list, test_dataset = csv_load_to_dataset(model_path, pretrained_model, fold_length)
    dataloader_list, test_dataloader = create_dataloader(dataset_list, test_dataset, model_path, pretrained_model, batch)
    train(dataloader_list, test_dataloader, model_path, pretrained_model, save_model, device, seed_val, epochs, fold_length)
    
    torch.save(model.state_dict(), model_path + save_model)


if __name__ == "__main__":
    main()