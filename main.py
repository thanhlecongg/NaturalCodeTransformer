import argparse
import os
import utils
from CodeInfilling.infilling import random_infilling, llm_infilling

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