from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
class LLM():
    def __init__(self, model_name):
        self.model_name = model_name
        self._create_model()
    
    def _create_model(self):
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name, 
                                                          device_map="auto")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model.eval()
        self.max_length = self.tokenizer.model_max_length

    def entropy(self, code):
        tokens_ids = self.tokenizer.encode(code, return_tensors="pt").squeeze().tolist()
        seq_len = len(tokens_ids)
        if seq_len > self.max_length:
            tokens_ids = tokens_ids[:self.max_length]
        input_ids = torch.tensor(tokens_ids)[None,:].to(device=device)
        target_ids = input_ids.clone().detach()
        with torch.no_grad():
            outputs = self.model(input_ids, labels=target_ids)
        
        return outputs.loss.mean().item()
    
class RNC():
    def __init__(self, model_name):
        self.model = LLM(model_name)
        
    def score(self, original_code, transformed_code):
        original_entropy = self.model.entropy(original_code)
        transformed_entropy = self.model.entropy(transformed_code)
        return (transformed_entropy - original_entropy)/original_entropy
    
    def batch_score(self, original, transformed_codes):
        scores = []
        original_entropy = self.model.entropy(original)
        for code in transformed_codes:
            transformed_entropy = self.model.entropy(code)
            scores.append((transformed_entropy - original_entropy)/original_entropy)
        return scores

