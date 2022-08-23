import torch

class ClassificationHead(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.dropout = torch.nn.Dropout(0.25)
        self.out_proj = torch.nn.Linear(768, 2)
    
    def forward(self, features):
        # 보통 분류기에선 start 토큰에 분류 결과를 담음
        x = features[:, 0, :]    # take <s> token (equiv. to [CLS])
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
        )
        self.labels = labels
        logits = self.classifier(outputs["last_hidden_state"])
        
        if labels is not None:
            loss_fct = torch.nn.CrossEntropyLoss()
            loss = loss_fct(logits, labels)
            return logits, loss
        else:
            return logits