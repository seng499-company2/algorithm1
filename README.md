# SENG 499 - Company 2 - Algorithm 1 

This repository contains a package ([_coursescheduler_](https://pypi.org/project/coursescheduler/)) that schedules 
the courses required for a software engineering degree at University of Victoria. The problem is implemented as a 
constraint satisfaction problem and an optimized backtracking search algorithm is used to find a valid schedule. 
This package was created for the Capstone SENG499 class: Company 2 Course Scheduler Project. 
Authored by the Company2-Algorithm1 sub-team.

## Install from PyPi Using PIP
Install this package into your environment from PyPi using `pip`.
```bash
$ pip install coursescheduler
```
The most recent available version of the package is uploaded to the PyPi index automatically as part of our CI/CD 
pipeline. To ensure that you are working with the most recent release, upgrade this module before integrating.
```bash
$ python3 -m pip install --upgrade coursescheduler
```

## Install from Local Archives
Clone this repo into your repository. Inside the algorithm 1 module directory,
build and install the package as shown below. Note: you must replace `0.0.1` with the correct version.
```bash
$ python3 -m build
$ pip3 install coursescheduler-0.0.1.tar.gz
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

## Dev
To make and test changes to the project, navigate into the root level directory 
`/path/to/algorithm1/`. After editing the project files, in order for the changes to take
effect you must reinstall the local package by the following cmd:
```bash
$ pip3 install . 
```
To run the tests
```bash
$ cd tests
$ python -m pytest
```

## Python Linter
To install Pylint on your device:
```bash
$ pip3 install black
```
To run the Black Python Linter:
```bash
$ black {python_script}.py
```
