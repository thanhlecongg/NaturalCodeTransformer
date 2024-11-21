from transformers import RobertaTokenizer, RobertaForMaskedLM, pipeline
from .substitution_utils import is_suitable
import os
from tqdm import tqdm   
from antlr4 import *
from .antlr.Java8Lexer import Java8Lexer
import itertools
from .substitution_utils import is_suitable, gen_random_string

class CodeBERTProbing():
    def __init__(self, name, top_k):
        self.name = name
        self.top_k = top_k
        self.model = RobertaForMaskedLM.from_pretrained("microsoft/codebert-base-mlm")
        self.tokenizer = RobertaTokenizer.from_pretrained("microsoft/codebert-base-mlm")
        self.fill_mask = pipeline('fill-mask', model=self.model, tokenizer=self.tokenizer, top_k=50)
    
    def predict(self, code, existing_var = []):
        outputs = self.fill_mask(code)

        try:
            candidates = [item['token_str'].strip() for item in outputs]
            filtered_candidates = []
            for cand in candidates:
                if cand not in filtered_candidates and is_suitable(cand, existing_var):
                    filtered_candidates.append(cand)
            return filtered_candidates[:5]
        except:
            occurences = {}
            
            for i in range(len(outputs)):
                for j in range(len(outputs[i])):
                    if outputs[i][j]["token_str"].strip() not in occurences:
                        occurences[outputs[i][j]["token_str"].strip()] = outputs[i][j]["score"] 
                    else:
                        occurences[outputs[i][j]["token_str"].strip()] += outputs[i][j]["score"] 

            sorted_occurences = dict(sorted(occurences.items(), key=lambda x: x[1], reverse=True))
            
            filtered_occurences = {}
            for cand in sorted_occurences:
                if is_suitable(cand, existing_var):
                    filtered_occurences[cand] = sorted_occurences[cand]
            
            return list(filtered_occurences.keys())[:self.top_k]


def random_infilling(input_dir, output_dir):    
    model = CodeBERTProbing("CodeBERT", 5)
    files = [f for f in os.listdir(input_dir) if f.endswith(".java")]

    for file in tqdm(files):
        file_name = file[:-5]    
        print("============================")
        print(file_name)
        new_path = os.path.join(output_dir, file_name + "_random.java")

        path = os.path.join(input_dir, file)
        ori_code = open(path, 'r').read()
        tokens = antlr_tokenize(ori_code)
        var_set = set()
        for _, t in enumerate(tokens):
            if t.startswith("___MASKED_"):
                var = t[10:-3]
                var_set.add(var)
                
        if len(var_set) == 0:
            continue
        
        substitute_candidate = {}
        existing_vars = set(tokens) | var_set

        new_code = ori_code
        for var in var_set: 
            new_var = gen_random_string(existing_vars)
            new_code = new_code.replace("___MASKED_" + var + "___", new_var)  

        with open(new_path, 'w') as f:
            f.write(new_code)
        exit()

def antlr_tokenize(code):
    codeStream = InputStream(code)
    lexer = Java8Lexer(codeStream)
    tokens = lexer.getAllTokens()
    return [t.text for t in tokens]


def generate_arrays(k, t):
    digits = range(t)  # Generate digits from 0 to j-1
    arrays = itertools.product(digits, repeat=k)  # Generate all possible combinations
    return list(arrays)

def generate_combinations(substitute_candidate):
    list_keys = list(substitute_candidate.keys())
    number_of_vars = len(list_keys)
    number_of_subs = len(list(substitute_candidate.values())[0])
    valid_combinations = []
    for combo in generate_arrays(number_of_vars, number_of_subs):
        substitute_combinations = {}
        existing_subs = []
        is_valid = True
        for idx, key in enumerate(list_keys):
            curr_sub = substitute_candidate[key][combo[idx]]
            if curr_sub in existing_subs:
                is_valid = False
                break
            existing_subs.append(curr_sub)
            substitute_combinations[key] = curr_sub
        if is_valid:
            valid_combinations.append([substitute_combinations, sum(combo)])
    
    sorted_combinations = sorted(valid_combinations, key=lambda x: x[1])
    return sorted_combinations

def truncate_code(code, mask_token="<mask>", max_length=512):
    mask_pos = code.find(mask_token)
    if mask_pos == -1:
        return code[:max_length]
    start_pos = max(0, mask_pos - (max_length // 5))
    end_pos = min(len(code), start_pos + (max_length // 5))
    truncated_code = code[start_pos:end_pos]
    if mask_token not in truncated_code:
        truncated_code = code[max(0, mask_pos - (max_length - len(mask_token))):mask_pos + len(mask_token)]
    return truncated_code

def llm_infilling(input_dir, output_dir):
    top_k = 3
    output_dirs = {}
    
    model = CodeBERTProbing("CodeBERT", 5)
    files = [f for f in os.listdir(input_dir) if f.endswith(".java")]

    for file in tqdm(files):
        file_name = file[:-5]    
        path = os.path.join(input_dir, file)
        ori_code = open(path, 'r').read()
        ctx_code = ori_code.replace("\n", " ")
        tokens = antlr_tokenize(ori_code)
        var_set = set()
        for _, t in enumerate(tokens):
            if t.startswith("___MASKED_"):
                var = t[10:-3]
                var_set.add(var)
                
        if len(var_set) == 0:
            continue
        
        substitute_candidate = {}
        existing_vars = set(tokens) | var_set

        for curr_var in var_set:
            masked_code = ctx_code.replace("___MASKED_" + curr_var + "___", "<mask>")
            for other_var in var_set:
                if other_var != curr_var:
                    masked_code = masked_code.replace("___MASKED_" + other_var + "___", other_var)
            masked_code = truncate_code(masked_code)
            substitute_candidate[curr_var] = model.predict(masked_code, existing_vars)
        
        combinations = generate_combinations(substitute_candidate)
        for idx in range(top_k):
            subs = combinations[idx][0]
            new_code = ori_code 
            for var in var_set:
                new_code = new_code.replace("___MASKED_" + var + "___", subs[var])
            new_path = os.path.join(output_dir, "{}_llm_{}.java".format(file_name, idx))
            with open(new_path, 'w') as f:
                f.write(new_code)
