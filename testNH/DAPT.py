from transformers import AutoModelForMaskedLM
from transformers import AutoTokenizer
from transformers import default_data_collator
from transformers import Trainer
from transformers import EarlyStoppingCallback
from transformers import TrainingArguments
from datasets import load_dataset
from huggingface_hub import notebook_login
import collections
import numpy as np
import json
import sys, os
sys.path.append(os.path.dirname(__file__))
from etc_modules import preprocessing

def tokenize_function(examples):
    result = tokenizer(examples['article'])
    result['word_ids'] = [result.word_ids(i) for i in range(len(result["input_ids"]))]
    return result

def group_texts(examples):
    # 모든 텍스트들을 결합
    concatenated_examples = {k:sum(examples[k], []) for k in examples.keys()}
    # 결합된 텍스트들에 대한 길이 구함
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    total_length = (total_length // 512) * 512
    result = {
        k: [t[i:i+512] for i in range(0, total_length, 512)]
        for k, t in concatenated_examples.items()
    }
    result['labels'] = result['input_ids'].copy()
    return result

def whole_word_masking_data_collator(features):
    for feature in features:
        word_ids = feature.pop("word_ids")

        # 단어와 해당 토큰 인덱스 간의 map 생성
        mapping = collections.defaultdict(list)
        current_word_index = -1
        current_word = None
        for idx, word_id in enumerate(word_ids):
            if word_id is not None:
                if word_id != current_word:
                    current_word = word_id
                    current_word_index += 1
                mapping[current_word_index].append(idx)

        # 무작위로 단어 마스킹
        mask = np.random.binomial(1, 0.2, (len(mapping),))
        input_ids = feature["input_ids"]
        labels = feature["labels"]
        new_labels = [-100] * len(labels)
        for word_id in np.where(mask)[0]:
            word_id = word_id.item()
            for idx in mapping[word_id]:
                new_labels[idx] = labels[idx]
                input_ids[idx] = tokenizer.mask_token_id

    return default_data_collator(features)

def loaddataset(file):
    dataset = load_dataset("csv", data_files=file)
    processed = dataset.map(preprocessing)
    tokenized_dataset = processed.map(tokenize_function, remove_columns=['company', 'title', 'article', 'opinion', 'firm', 'date'])
    lm_datasets = tokenized_dataset.map(group_texts)
    downsampled_dataset = lm_datasets["train"].train_test_split(test_size=0.1, seed=42)
    return downsampled_dataset

def train(batch_size, epochs, downsampled_dataset, model_name, pretrained):
    logging_steps = len(downsampled_dataset["train"]) // batch_size
    model = AutoModelForMaskedLM.from_pretrained(pretrained)
    training_args = TrainingArguments(
        output_dir=f"{model_name}-finetuned-wholemasking20",
        num_train_epochs=epochs,
        overwrite_output_dir=True,
        evaluation_strategy="steps",
        eval_steps=500,
        save_total_limit=3,
        learning_rate=2e-5,
        weight_decay=0.01,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        push_to_hub=True,
        fp16=True,
        logging_steps=logging_steps,
        remove_unused_columns=False,
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=downsampled_dataset["train"],
        eval_dataset=downsampled_dataset["test"],
        data_collator=whole_word_masking_data_collator,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=5)]
    )

    trainer.train()
    trainer.push_to_hub()

def main():
    json_file = open("./DAPT_config.json", encoding="utf-8")
    key_dict = json.loads(json_file.read())
    model_name = key_dict["model_name"]
    data_file = key_dict["data_file_path"]
    batch_size = key_dict["batch"]
    epochs = key_dict["epochs"]
    if model_name == 'koBERT':
        pretrained = 'monologg/kobert'
    else:
        pretrained = 'klue/roberta-large'

    global tokenizer
    tokenizer = AutoTokenizer.from_pretrained(pretrained)
    downsampled_dataset = loaddataset(data_file)
    notebook_login()
    train(batch_size, epochs, downsampled_dataset, model_name, pretrained)

if __name__ == "__main__":
    main()