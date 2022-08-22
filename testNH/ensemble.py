import pandas as pd
import numpy as np

KBALBERT = pd.read_csv("KB-ALBERT_ensemble_inferenced.csv")
koBERT = pd.read_csv("koBERTinferenced.csv")
roBERTa = pd.read_csv("roBERTainferenced.csv")

KBALBERT = KBALBERT["pred_rate"]
koBERT = koBERT["pred_rate"]
roBERTa = roBERTa["pred_rate"]

probabilities = [list() for _ in range(3)]
probabilities[0].append(KBALBERT)
probabilities[1].append(koBERT)
probabilities[2].append(roBERTa)

ensemble_prob = np.mean(probabilities, axis=0, dtype=np.float64)
ensemble_pred = (ensemble_prob > 50).astype(np.int32)

convert_pred = list(map(lambda x: "매수" if x == 1 else "매도", ensemble_pred))
convert_prob = list(map(lambda x: np.round(x, 2) if x > 50 else np.round(100 - x, 2), ensemble_prob))

inference_dataframe = pd.read_csv("inferencedatasetprocessed.csv")
inference_dataframe = inference_dataframe.drop(labels="Unnamed: 0", axis=1)
inference_dataframe["predictions"] = convert_pred
inference_dataframe["pred_rate"] = convert_prob
inference_dataframe.to_csv(f"./data/final_ensemble_inferenced.csv", index=False)