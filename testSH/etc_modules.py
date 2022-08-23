import numpy as np
import pandas as pd
import torch
import random


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
    
def flat_accuracy(preds, labels):
    pred_flat = np.argmax(preds, axis=1).flatten()
    labels_flat = labels.flatten()
    
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

def set_seed(seed_val):
    random.seed(seed_val)
    np.random.seed(seed_val)
    torch.manual_seed(seed_val)
    torch.cuda.manual_seed_all(seed_val)