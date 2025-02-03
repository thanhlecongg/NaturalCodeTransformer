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

For detailed mapping between rule ID and semantic-preserving transformation rule, please see [RULE](https://github.com/thanhlecongg/NaturalCodeTransformer/blob/main/RULE.md)

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



