import argparse
import os
import utils
import json
from tqdm import tqdm

from CodeInfilling.infilling import random_infilling, llm_infilling
from CodeNaturalnessEvaluator.evaluator import RNC
def run_transform(args):
    print("Running transform module")
    print("Info path: ", args.info_path)
    print("Output directory: ", args.output_dir)
    
    if args.transform_rules == 'all':
        print("Applying all transform rules")
        transform_rules = [i + 1 for i in range(0, 23)]
    else:
        transform_rules = [int(rule) for rule in args.transform_rules.split(",")]
        print("Applying transform rules: ", transform_rules)
    
    info_path = os.path.abspath(args.info_path)
    CMD = "java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o {} -r {} -f {}"
    for rule in transform_rules:
        output_dir = os.path.join(args.output_dir, "rule_" + str(rule))
        output_dir = os.path.abspath(output_dir) + "/"
        os.makedirs(output_dir, exist_ok=True)
        cmd = CMD.format(output_dir, rule, info_path)
        print("Running command: ", cmd)
        output = utils.execute_command(cmd)
        print(output)
    print("Transform module completed")
    
def run_infilling(args):
    os.makedirs(args.output_dir, exist_ok=True)
    assert args.fill_type != "llm" or args.top_k is not None, "Top k must be provided for llm infilling" 
    if args.fill_type == 'random':
        random_infilling(args.input_dir, args.output_dir)
    elif args.fill_type == 'llm':
        llm_infilling(args.input_dir, args.output_dir, args.top_k)
    else:
        print("Invalid fill type. Please select either random or llm")

def run_evaluation(args):
    print("Running evaluation module")
    
    evaluator = RNC(model_name=args.model_name) 
    
    ### Load meta data 
    with open(args.info_path, 'r') as f:
        data = json.load(f)
        
    meta_data = {}
    for d in data:
        meta_data[d["instanceId"]] = d
        
    ### Group transformed programs by class name
    transformed_programs = {}
    for transform_id in os.listdir(args.transformed_dir):
        transform_dir = os.path.join(args.transformed_dir, transform_id)
        if not os.path.isdir(transform_dir):
            continue
        for file in os.listdir(transform_dir):
            class_name = file.split(".")[0].split("_")[0]
            file_path = os.path.join(transform_dir, file)
            file_id = transform_id + "_" + file.split(".")[0]
            if class_name not in transformed_programs:
                transformed_programs[class_name] = []
            transformed_programs[class_name].append((file_path, file_id))
    
    fw = open(args.output_path, 'w')
    
    ### Evaluate transformed programs
    evaluation_results = []
    for class_name in tqdm(transformed_programs):
        original_fp = meta_data[class_name]["sourceFile"]
        original_code = open(original_fp, 'r').read()
        transformed_codes = []
        program_ids = []
        for file_path, file_id in transformed_programs[class_name]:
            program_ids.append(file_id)
            transformed_codes.append(open(file_path, 'r').read())
        
        try:
            scores = evaluator.batch_score(original_code, transformed_codes)
            for program_id, scores in zip(program_ids, scores):
                fw.write(f"{program_id} {scores}\n")
        except Exception as e:
            print(f"Error evaluating class {class_name}")
            print(e)
    
    fw.close()
        
        
        
        
        
    
    pass

def main():
    parser = argparse.ArgumentParser(description="Main script to call different modules.")
    subparsers = parser.add_subparsers(dest='module', required=True, help="Module to run")

    # Subparser for transform
    parser_transform = subparsers.add_parser('transform', help='Run transform module')
    parser_transform.add_argument('-i', '--info_path', type=str, required=True, help='Path to the info file')
    parser_transform.add_argument('-o', '--output_dir', type=str, required=True, help='Output directory to store transformed programs')
    parser_transform.add_argument('-r', '--transform_rules', type=str, default='all', help='Comma separated list of transform rules to apply')

    # Subparser for infilling
    parser_infilling = subparsers.add_parser('infilling', help='Run infilling module')
    parser_infilling.add_argument('-i', '--input_dir', type=str, help='Input directory containing transformed programs')
    parser_infilling.add_argument('-o', '--output_dir', type= str, help='Output directory to store infilled programs')
    parser_infilling.add_argument('-f', '--fill_type', type=str, help='Type of infilling to apply. Options: random, llm')
    parser_infilling.add_argument('-k', '--top_k', default= None, type=int, help='Top k candidates to consider for llm infilling')
    
    # Subparser for evaluation
    parser_evaluation = subparsers.add_parser('evaluation', help='Run evaluation module')
    parser_evaluation.add_argument('-i', '--info_path', type=str, required=True, help='Path to the info file')
    parser_evaluation.add_argument('-t', '--transformed_dir', type=str, required=True, help='Directory containing transformed programs')
    parser_evaluation.add_argument('-o', '--output_path', type=str, required=True, help='Output path to store evaluation results')
    parser_evaluation.add_argument('-m', '--model_name', default="codellama/CodeLlama-7b-hf", type=str, help='Model name for naturalness evaluation')
    
    args = parser.parse_args()

    if args.module == 'transform':
        run_transform(args)
    elif args.module == 'infilling':
        run_infilling(args)
    elif args.module == 'evaluation':
        run_evaluation(args)
    else:
        print("Invalid module")

if __name__ == "__main__":
    main()