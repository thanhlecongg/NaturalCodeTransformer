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
Transformed programs are stored at results/rules_{i} for i-th rule and expected logs should be:
```
Running transform module
Info path:  sample/input.json
Output directory:  results
Applying all transform rules
Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_1/ -r 1 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...
Whole file is parsed! begin rewriting
Whole file is parsed! begin rewriting
==>result is replaced by ___MASKED_result
==>nums is replaced by ___MASKED_nums
==>result is replaced by ___MASKED_result
==>nums is replaced by ___MASKED_nums
==>i is replaced by ___MASKED_i
==>i is replaced by ___MASKED_i
==>indices is replaced by ___MASKED_indices
==>indices is replaced by ___MASKED_indices
/data/gpfs/NaturalCodeTransformer/results/rule_1/Data1.java      reWrited successfully!
/data/gpfs/NaturalCodeTransformer/results/rule_1/Data1.java      reWrited successfully!

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_2/ -r 2 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...
/data/gpfs/NaturalCodeTransformer/results/rule_2/Data1.java      reWrited successfully!
/data/gpfs/NaturalCodeTransformer/results/rule_2/Data1.java      reWrited successfully!

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_3/ -r 3 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_4/ -r 4 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_5/ -r 5 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_6/ -r 6 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_7/ -r 7 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_8/ -r 8 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_9/ -r 9 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_10/ -r 10 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_11/ -r 11 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_12/ -r 12 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_13/ -r 13 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...
Whole file is parsed! begin rewriting
Whole file is parsed! begin rewriting

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_14/ -r 14 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_15/ -r 15 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_16/ -r 16 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_17/ -r 17 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_18/ -r 18 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...
class org.eclipse.jdt.core.dom.PostfixExpression
class org.eclipse.jdt.core.dom.PostfixExpression

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_19/ -r 19 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_20/ -r 20 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_21/ -r 21 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_22/ -r 22 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...

Running command:  java -jar CodeTransform/target/JavaTransformation-1.0-SNAPSHOT.jar -o /data/gpfs/NaturalCodeTransformer/results/rule_23/ -r 23 -f /data/gpfs/NaturalCodeTransformer/sample/input.json
Code Transform
Processing: Data1
Processing: Data2
Processing: Data1
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Processing: Data2
File path: /data/gpfs/NaturalCodeTransformer/sample/code/Data1.java
Parsing code...
Parsing code...
/data/gpfs/NaturalCodeTransformer/results/rule_23/Data1.java     reWrited successfully!
/data/gpfs/NaturalCodeTransformer/results/rule_23/Data1.java     reWrited successfully!
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
