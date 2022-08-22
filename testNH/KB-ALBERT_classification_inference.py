import torch
import copy
import gc
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

def load_models(model_name_list):
    load_model_list = list()

    for model_name in model_name_list:
        load_model = copy.deepcopy(AInalyst(pretrained_model=albert))
        load_model = torch.nn.DataParallel(load_model)
        load_model.to(device)

        now_state = torch.load(f"./models/{model_name}")
        load_model.load_state_dict(now_state)
        load_model.eval()

        load_model_list.append(load_model)
    return load_model_list

def inference_tokenized_fn(data):
    outputs = tokenizer(data["article"], padding="max_length", max_length=512, truncation=True)
    return outputs

def dataloader(file):
    inference_dataset = load_dataset("csv", data_files=file)["train"]
    inference_dataset = inference_dataset.map(inference_tokenized_fn,
                                              remove_columns=["Unnamed: 0", "company", "title", "opinion", "firm", "date", "article"])
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

    inference_dataloader = torch.utils.data.DataLoader(
        inference_dataset,
        sampler=torch.utils.data.SequentialSampler(inference_dataset),
        batch_size=1,
        collate_fn=data_collator,
    )
    return inference_dataloader

def inference(inference_dataloader, load_model_list, file):
    probabilities = [list() for _ in model_name_list]
    predictions = [list() for _ in model_name_list]

    for step, batch in enumerate(tqdm(inference_dataloader, desc="inference", mininterval=0.1)):
        batch_input_ids = batch["input_ids"].to(device)
        batch_attention_mask = batch["attention_mask"].to(device)

        for idx, load_model in enumerate(load_model_list):
            with torch.no_grad():
                logits = load_model(
                    input_ids=batch_input_ids,
                    attention_mask=batch_attention_mask,
                )

                prob = torch.nn.functional.softmax(logits, dim=-1)
                predict = torch.argmax(prob, axis=1)

                if predict == 1:
                    prob = np.round(np.max(prob.detach().cpu().numpy(), axis=1) * 100, 2)
                else:
                    prob = np.round((1 - np.max(prob.detach().cpu().numpy(), axis=1)) * 100, 2)

                predict = predict.detach().cpu().numpy()

                probabilities[idx].append(prob[0])
                predictions[idx].append(predict[0])

    ensemble_prob = np.mean(probabilities, axis=0, dtype=np.float64)
    ensemble_pred = (ensemble_prob > 50).astype(np.int32)

    inference_dataframe = pd.read_csv(file)

    convert_pred = list(map(lambda x: "매수" if x == 1 else "매도", ensemble_pred))

    inference_dataframe = inference_dataframe.drop(labels="Unnamed: 0", axis=1)
    inference_dataframe["predictions"] = convert_pred
    inference_dataframe["pred_rate"] = ensemble_prob
    inference_dataframe.to_csv("KB-ALBERT_ensemble_inferenced.csv", index=False)


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name_list = [
    "kbalbert_agument_epoch1_fold5_without_papago.pt",
    "kbalbert_agument_epoch3_fold5_without_papago.pt",
    "kbalbert_agument_epoch5_fold5_without_papago.pt",
    "kbalbert_origin_epoch1_fold5.pt",
    "kbalbert_origin_epoch3_fold5.pt",
]
kb_albert_model_path = "kb-albert-char-base-v2"
albert = AutoModel.from_pretrained(kb_albert_model_path)
tokenizer = AutoTokenizer.from_pretrained(kb_albert_model_path)
tokenizer.truncation_side = "left"
load_model_list = load_models(model_name_list)
file = 'inferencedatasetprocessed.csv'
inference_dataloader = dataloader(file)
inference(inference_dataloader, load_model_list, file)

gc.collect()
torch.cuda.empty_cache()