# NaturalCodeTransformer: Natural Code Transformation Tool for Java
This repository implement a tool that transforms Java code snippets for generating semantic-preserving programs. 

This tool include three components:
- CodeTransform: this component is used to transform original Java programs into new programs using semantic-preserving transformations. A part of this module is built upon [SPAT](https://github.com/Santiago-Yu/SPAT).
- CodeInfilling: Some semantic-preserving transformations including: VariableRenaming (ID-1), For2While (ID-2), and InfixDividing (ID-17) requires the substitutions of Variable Names. This component is used to suggest suitable variable names for these transformation
is used to fill masked code (e.g., variable name) using Pre-trained Language Models to enhance naturalness of transformed code
- CodeNaturalnessEvaluator: is used to assess the naturalness of semantic-preserving transformations

## Installations

### Prerequisites

Apache Maven 3.9.9 
Openjdk 23.0.1 2024-10-15
Python 3.10

### Python Enviroments

### Re-build Java Transformation
If you want to rebuild `CodeTransform` module, please use the following command:
```
mvn clean package
```

## Usage

### Transform

To use transform module, please use the following command:
```
usage: python3 main.py transform [-h] -i INFO_PATH -o OUTPUT_DIR [-r TRANSFORM_RULES]

options:
  -h, --help            show this help message and exit
  -i INFO_PATH, --info_path INFO_PATH
                        Path to the info file
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory to store transformed programs
  -r TRANSFORM_RULES, --transform_rules TRANSFORM_RULES
                        Comma separated list of transform rules to apply
```

For a detailed mapping between rule IDs and semantic-preserving transformation rules, please refer to [RULE](https://github.com/thanhlecongg/NaturalCodeTransformer/blob/main/RULE.md).

The information file is a JSON file that contains a list of dictionaries, each providing details about the target programs. The structure of the information file is as follows:

```
[
    {
        "instanceId": "Data1",
        "sourceFile": "data/methods/Data1.java",
        "targetLines": []
    },
    {
        "instanceId": "Data2",
        "sourceFile": "data/methods/Data2.java",
        "targetLines": []
    },
    ...
]
```

In this template, `"instanceId"` represents the name of the Java file, `"sourceFile"` specifies the path to the corresponding `.java` file, and `"targetLines"` contains the lines of code targeted for transformation. By default, `"targetLines"` is an empty list, indicating that all lines in the file will be considered for transformation. However, if specific lines are specified, the tool will restrict transformations to the declared target lines.

### Infilling

To use infilling module, please use the following command:

```
usage: python3 main.py infilling [-h] [-i INPUT_DIR] [-o OUTPUT_DIR] [-f FILL_TYPE]

options:
  -h, --help            show this help message and exit
  -i INPUT_DIR, --input_dir INPUT_DIR
                        Input directory containing transformed programs
  -o OUTPUT_DIR, --output_dir OUTPUT_DIR
                        Output directory to store infilled programs
  -f FILL_TYPE, --fill_type FILL_TYPE
                        Type of infilling to apply. Options: random, llm
```

### Example Usage

Please use data provide in `sample` folder to run an example of our tool. 

1. Generate transformation with `CodeTransform` by using
```
python3 main.py transform -i sample/input.json -o results -r all
```

## Citations
Please cite the following article if you find this tool to be useful:

```
@article{10.1145/3716167,
author = {Le-Cong, Thanh and Nguyen, Thanh-Dat and Le, Bach and Murray, Toby},
title = {Towards Reliable Evaluation of Neural Program Repair with Natural Robustness Testing},
year = {2025},
publisher = {Association for Computing Machinery},
address = {New York, NY, USA},
issn = {1049-331X},
url = {https://doi.org/10.1145/3716167},
doi = {10.1145/3716167},
note = {Just Accepted},
journal = {ACM Trans. Softw. Eng. Methodol.},
month = feb,
}
```

In addition, kindly ensure that [SPAT](https://github.com/Santiago-Yu/SPAT) is acknowledged in accordance with the guidelines provided.
