import sys, os
import copy
import json
import numpy as np
import torch
from tqdm import tqdm
from transformers import AutoModel, AutoModelForSequenceClassification, AutoConfig

sys.path.append(os.path.dirname(__file__))
import model, data_control, etc_modules


def inference(inference_dataloader, device, model_path, pretrained_model_name, pretrained_model_path, inference_model_list):
    load_model_list = list()
    
    if pretrained_model_name == "kbalbert":
        pretrained_model = AutoModel.from_pretrained(pretrained_model_path)
        for model_name in inference_model_list:
            load_model = copy.deepcopy(model.AInalyst(pretrained_model=pretrained_model))
            load_model = torch.nn.DataParallel(load_model)
            load_model.to(device)
            load_model.load_state_dict(torch.load(model_path + model_name))
            load_model.eval()

            load_model_list.append(load_model)
    else:
        for model_name in inference_model_list:
            config = AutoConfig.from_pretrained(pretrained_model_path)
            config.num_labels = 2
            load_model = copy.deepcopy(AutoModelForSequenceClassification.from_pretrained(pretrained_model_path,
                                                                                          config=config))
            load_model.to(device)
            load_model.load_state_dict(torch.load(model_path + model_name))
            load_model.eval()

            load_model_list.append(load_model)

    probabilities = [list() for _ in inference_model_list]

    for step, batch in enumerate(tqdm(inference_dataloader, desc="inference", mininterval=0.1)):            
        batch_input_ids = batch["input_ids"].to(device)
        batch_attention_mask = batch["attention_mask"].to(device)

        for idx, load_model in enumerate(load_model_list):
            with torch.no_grad():
                if pretrained_model_name == "kbalbert":
                    logits = load_model(
                        input_ids = batch_input_ids,
                        attention_mask = batch_attention_mask,
                    )
                else:
                    logits = load_model(
                        input_ids=batch_input_ids,
                        attention_mask=batch_attention_mask,
                    ).logits

                prob = torch.nn.functional.softmax(logits, dim=-1)
                predict = torch.argmax(prob, axis=1)

                if predict == 1:
                    prob = np.round(np.max(prob.detach().cpu().numpy(), axis=1) * 100, 2)
                else:
                    prob = np.round((1 - np.max(prob.detach().cpu().numpy(), axis=1)) * 100, 2)

                probabilities[idx].append(prob[0])

    return probabilities
    
def main():    
    json_file = open("./inference_config.json", encoding="utf-8")
    key_dict = json.loads(json_file.read())

    data_file_path = key_dict["data_file_path"]
    save_file_path = key_dict["save_file_path"]
    pretrained_model = key_dict["pretrained_model"]
    model_path = key_dict["model_path"]
    inference_model_list = key_dict["inference_model_list"]
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    all_models_probabilities = list()
    voting_probabilities = list()
    
    for pretrained in pretrained_model:
        inference_dataloader = data_control.create_inference_dataloader(data_file_path, pretrained, pretrained_model[pretrained])
        all_models_probabilities.append(inference(inference_dataloader, device, model_path,
                                                  pretrained, pretrained_model[pretrained], inference_model_list[pretrained]))
    for probabilities in all_models_probabilities:
        voting_probabilities.append(etc_modules.soft_voting(probabilities))
        
    etc_modules.save_csv_file(data_file_path, save_file_path, voting_probabilities)

    
if __name__ == "__main__":
    main()   