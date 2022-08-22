import torch
import numpy as np
import pandas as pd
from transformers import AutoModel, AutoTokenizer, DataCollatorWithPadding
from datasets import load_dataset
from sklearn.model_selection import train_test_split, StratifiedKFold
from datasets import load_dataset
from transformers import DataCollatorWithPadding
import random
from tqdm import tqdm

class ClassificationHead(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.dropout = torch.nn.Dropout(0.25)
        self.out_proj = torch.nn.Linear(768, 2)

    def forward(self, features):
        # 보통 분류기에선 start 토큰에 분류 결과를 담음
        x = features[:, 0, :]  # take <s> token (equiv. to [CLS])
        x = x.reshape(-1, x.size(-1))
        x = self.dropout(x)

        x = self.out_proj(x)
        return x


class AInalyst(torch.nn.Module):
    def __init__(self, pretrained_model):
        super(AInalyst, self).__init__()
        self.pretrained = pretrained_model
        self.classifier = ClassificationHead()

    def forward(self, input_ids=None, attention_mask=None, labels=None):
        outputs = self.pretrained(
            input_ids=input_ids,
            attention_mask=attention_mask,
            # labels=labels
        )
        self.labels = labels
        logits = self.classifier(outputs["last_hidden_state"])
        # prob = torch.nn.functional.softmax(logits, dim=-1)

        if labels is not None:
            loss_fct = torch.nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)
            return logits, loss
        else:
            return logits

def makekfoldtraindata(file, fold_length=5):
    all_data = pd.read_csv(file)
    train_data, test_data = train_test_split(all_data, test_size=0.2, random_state=42, stratify=all_data[["label"]])

    test_data["labels"] = test_data["label"]
    test_data = test_data.drop(labels=["filename", "length", "label"], axis=1)

    X = train_data.drop(labels=["filename", "length", "label"], axis=1)
    y = train_data["label"]

    skf = StratifiedKFold(n_splits=fold_length, shuffle=True, random_state=42)
    for fold_number, (train, valid) in enumerate(skf.split(X, y), 1):
        X_train, X_valid = X.iloc[train], X.iloc[valid]
        y_train, y_valid = y.iloc[train], y.iloc[valid]

        fold_train = X_train.loc[:]
        fold_train["labels"] = y_train

        fold_valid = X_valid.loc[:]
        fold_valid["labels"] = y_valid

        fold_train.to_csv(f"train_data_fold{fold_number}.csv", index=False)
        fold_valid.to_csv(f"valid_data_fold{fold_number}.csv", index=False)

    test_data.to_csv("test_data.csv", index=False)

def tokenized_fn(data):
    outputs = tokenizer(data["article"], padding="max_length", max_length=512, truncation=True)
    outputs["labels"] = data["labels"]
    return outputs

def dataloader(fold_length=5):
    dataset_list = list()
    for fold_number in range(1, fold_length + 1):
        train_dataset = load_dataset("csv", data_files=f"train_data_fold{fold_number}.csv")["train"]
        valid_dataset = load_dataset("csv", data_files=f"valid_data_fold{fold_number}.csv")["train"]

        train_dataset = train_dataset.map(tokenized_fn, remove_columns=["article"])
        valid_dataset = valid_dataset.map(tokenized_fn, remove_columns=["article"])

        dataset_list.append([train_dataset, valid_dataset])

    test_dataset = load_dataset("csv", data_files=f"./data/test_data.csv")["train"]
    test_dataset = test_dataset.map(tokenized_fn, remove_columns=["article"])

    batch_size = 16

    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    dataloader_list = list()
    for train_fold, valid_fold in dataset_list:
        train_dataloader = torch.utils.data.DataLoader(
            train_fold,
            sampler=torch.utils.data.RandomSampler(train_fold),
            batch_size=batch_size,
            collate_fn=data_collator,
        )

        validation_dataloader = torch.utils.data.DataLoader(
            valid_fold,
            sampler=torch.utils.data.SequentialSampler(valid_fold),
            batch_size=batch_size,
            collate_fn=data_collator,
        )

        dataloader_list.append([train_dataloader, validation_dataloader])

    test_dataloader = torch.utils.data.DataLoader(
        test_dataset,
        sampler=torch.utils.data.SequentialSampler(test_dataset),
        batch_size=batch_size,
        collate_fn=data_collator,
    )
    return dataloader_list, test_dataloader

def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def train(dataloader_list, model, epochs=1, fold_length=5):
    for epoch in range(epochs):
        print(f"============ Epoch {epoch + 1}/{epochs} ============")
        print("Training...")

        for fold_number, (train_dataloader, validation_dataloader) in enumerate(dataloader_list, 1):
            print(f"===== Epoch {epoch + 1}/{epochs} - Fold {fold_number}/{fold_length} =====")
            total_train_loss = 0
            model.train()

            for step, batch in enumerate(train_dataloader):
                batch_input_ids = batch["input_ids"].to(device)
                batch_attention_mask = batch["attention_mask"].to(device)
                batch_labels = batch["labels"].to(device)

                model.zero_grad()

                logits, loss = model(
                    input_ids=batch_input_ids,
                    attention_mask=batch_attention_mask,
                    labels=batch_labels,
                )

                if isParallel:
                    loss = loss.mean()

                total_train_loss += loss.item()
                loss.backward()
                optimizer.step()

                # if step % 1000 == 0 and not step == 0:
                #     print("step : {:>5,} of {:>5,} loss: {:.5f}".format(step, len(train_dataloader), loss.item()))

            avg_train_loss = total_train_loss / len(train_dataloader)
            print()
            print(" Average training loss: {0:.5f}".format(avg_train_loss))

            # Validation
            print()
            print("Running Validation...")

            model.eval()
            total_eval_accuracy = 0
            total_eval_loss = 0
            nb_eval_steps = 0

            for step, batch in enumerate(validation_dataloader):
                batch_input_ids = batch["input_ids"].to(device)
                batch_attention_mask = batch["attention_mask"].to(device)
                batch_labels = batch["labels"].to(device)

                with torch.no_grad():
                    logits, loss = model(
                        input_ids=batch_input_ids,
                        attention_mask=batch_attention_mask,
                        labels=batch_labels,
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
        print(f"===== Epoch {epoch + 1}/{epochs} - Test =====")
        print()
        print("Running Test...")

        model.eval()
        total_test_accuracy = 0
        total_test_loss = 0
        nb_test_steps = 0

        for step, batch in enumerate(test_dataloader):
            batch_input_ids = batch["input_ids"].to(device)
            batch_attention_mask = batch["attention_mask"].to(device)
            batch_labels = batch["labels"].to(device)

            with torch.no_grad():
                logits, loss = model(
                    input_ids=batch_input_ids,
                    attention_mask=batch_attention_mask,
                    labels=batch_labels,
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
    torch.save(model.state_dict(), "kbalbert_origin_epoch1_fold5.pt")


kb_albert_model_path = "kb-albert-char-base-v2"
albert = AutoModel.from_pretrained(kb_albert_model_path)
tokenizer = AutoTokenizer.from_pretrained(kb_albert_model_path)
tokenizer.truncation_side = "left"
file = 'traindataset.csv'
makekfoldtraindata(file)
dataloader_list, test_dataloader = dataloader()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = AInalyst(pretrained_model=albert)
model.to(device)
model = torch.nn.DataParallel(model)
isParallel = True
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

gc.collect()
torch.cuda.empty_cache()

train(dataloader_list, model)