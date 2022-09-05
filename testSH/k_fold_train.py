import sys, os
import json
import torch
from transformers import AutoModel

sys.path.append(os.path.dirname(__file__))
import model, data_control, etc_modules

    
def train(dataloader_list, test_dataloader, model_path, pretrained_model, save_model, device, seed_val, epochs, fold_length):
    pretrained = AutoModel.from_pretrained(model_path + pretrained_model) 

    train_model = model.AInalyst(pretrained_model=pretrained)
    train_model.to(device)
    train_model = torch.nn.DataParallel(train_model)
    isParallel = True
    optimizer = torch.optim.AdamW(train_model.parameters(), lr=1e-5)

    etc_modules.set_seed(seed_val)

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
                    total_eval_accuracy += etc_modules.flat_accuracy(logits, label_ids)

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
                total_test_accuracy += etc_modules.flat_accuracy(logits, label_ids)

        avg_test_accuracy = total_test_accuracy / len(test_dataloader)
        print()
        print(" Test Accuracy: {0:.5f}".format(avg_test_accuracy))
        print()
        
    torch.save(train_model.state_dict(), model_path + save_model)

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
    
    all_data = data_control.load_dataframe(data_path, data_file)
    data_control.data_split(all_data, data_path, fold_length)   
    
    dataset_list, test_dataset = data_control.load_csv_to_dataset(model_path, pretrained_model, fold_length)
    dataloader_list, test_dataloader = data_control.create_train_dataloader(dataset_list, test_dataset, model_path, pretrained_model, batch)
    train(dataloader_list, test_dataloader, model_path, pretrained_model, save_model, device, seed_val, epochs, fold_length)


if __name__ == "__main__":
    main()