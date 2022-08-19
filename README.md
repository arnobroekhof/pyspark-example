
# PySpark example

![Test Build](https://github.com/arnobroekhof/pyspark-example/actions/workflows/test.yml/badge.svg)


*NOTE*: 
This is an example boilerplate project for a PySpark Project setup

including

* tests ( running in Github Actions and Local )
* mypy
* black
* linting

## Documentation


### requirements:

* Java 1.8
* Linux or MacOS
* pyenv or Python 3.7
* docker

### Getting started  

1. make the virtualenv 
```
make venv
```

2. init the dependencies
```
source .venv/bin/activate
make init-deps-dev
```

3. init the minio s3 container
```
make test-containers
```

4. run the tests
```
make test
```

### Directory Layout
```
pyspark-example
├── Makefile                --> GNU Makefile with all commands
├── README.md               --> This file
├── requirements-dev.txt    --> Development requirements
├── requirements.txt        --> Main Requirements
├── src                     --> Directory with python src 
│   └── example             --> example python package
│       ├── __init__.py     --> package init file
│       └── main.py         --> file with main code
└── tests                   --> directory with python tests
    ├── s3                  --> directory with S3 testing
    │   └── test_s3.py      --> test file for s3 type of actions
    ├── simple              --> directory with a simple test
    │   └── test_simple.py  --> test file with a simple test
    └── testdata            --> testdata directory
        └── creditcard.csv.zip  --> testdata set from Kaggle https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud

```

