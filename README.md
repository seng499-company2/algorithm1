# SENG 499 - Company 2: Algorithm 1 

This repository contains a package ([_coursescheduler_](https://pypi.org/project/coursescheduler/)) that schedules 
the courses required for a software engineering degree at University of Victoria. The problem is implemented as a 
constraint satisfaction problem and an optimized backtracking search algorithm is used to find a valid schedule. 
This package was created for the Capstone SENG499 class: Company 2 Course Scheduler Project. 
Authored by the Company2 Algorithm1 sub-team.

## Prerequisites
This package requires Python 3.9 or higher. In this README, it is assumed that `python` and `pip` will use Python 3.9. 
To check your Python version, you can run the following command:
```bash
$ python --version  # Should output "Python 3.9.0" or higher
```
To check your pip version, you can run the following command:
```bash
$ pip --version  # Should output some version of pip and "python 3.9" or higher
```

## Install from PyPi Using PIP
Install this package into your environment from PyPi using `pip`.
```bash
$ pip install coursescheduler
```
The most recent available version of the package is uploaded to the PyPi index automatically as part of our CI/CD 
pipeline. To ensure that you are working with the most recent release, upgrade this module before integrating.
```bash
$ python -m pip install --upgrade coursescheduler
```

## Install from Local Archives
Clone this repo into your repository. Inside the algorithm 1 module directory,
build and install the package as shown below. Note: you must replace `0.1.0` with the correct version.
```bash
$ python -m build
$ pip install coursescheduler-0.1.0.tar.gz
```

## Usage
Once installed, the algorithm can be imported and called with `generate_schedule`, as shown below. `generate_schedule` 
expects two parameters and returns a single output, all of which are Python dictionaries. 
The API specification 
can be found [here](https://docs.google.com/document/d/163L7pv6w5Z38rUrl2EwRJq-A9ZLllCIO9uYbUkdxi2s/edit?usp=sharing).
```python
from coursescheduler import generate_schedule
schedule = generate_schedule(professors, schedule)
```

A third parameter, `debug`, can be included. If set to True, `professors` and/or `schedule` can be set to `None` and the algorithm will use mock data.
```python
schedule = generate_schedule(None, None, True)  # Uses mock data for professors and schedule
schedule = generate_schedule(professors, None, True)  # Uses mock data for schedule
schedule = generate_schedule(None, schedule, True)  # Uses mock data for professors
```

There are also functions that will validate input data according to the spec:
```python
from coursescheduler import validate_professor_structure, validate_professors_structure, validate_schedule_structure
validate_professor_structure(professor)    # One Professor dict
validate_professors_structure(professors)  # A list of Professor dicts
validate_schedule_structure(schedule)      # A Schedule dict
```
If the input is valid according to the spec, these functions will return `True`.
If there is a spec violation, a `SchemaError` will be raised. A second parameter can be passed to all three validate functions called `print_output`, which is set to `True` by default.
If `print_output` is `True` and the input is valid, a success message will be printed to the console.

## Dev
To make and test changes to the project, navigate into the root level directory 
`/path/to/algorithm1/`. After editing the project files, in order for the changes to take
effect you must reinstall the local package by the following cmd:
```bash
$ pip install . 
```
To run the tests, run the following command:
```bash
$ cd tests
$ python -m pytest
```

## Python Linter
We follow the _PEP8_ style guide, and we use _flake8_ to lint our code.

To install _flake8_, run the following command:
```bash
$ pip install flake8
```
To run _flake8_, run the following command:
```bash
$ python -m flake8 [file or directory]
```

We recommend using the code formatter [black](https://black.readthedocs.io/en/stable/index.html):
```bash
$ pip install black
```
To run _black_:
```bash
$ python -m black [file or directory]
```
