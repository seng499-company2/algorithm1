# SENG 499 - Company 2 - Algorithm 1 

This repository contains a package, [Course-Scheduler](https://pypi.org/project/coursescheduler/), for
that returns a course schedule for three terms of Software Engineering courses at UVic. The Course Scheduler uses the 
Constraint Satisfaction Problem (CSP) Algorithm to determine the hard constraint of the schedule, and produces a schedule 
that adheres to the constraints. The scheduler also takes into account soft constraints for professor preferences, 
however, these constraints are not always fulfilled. 

This package was created for the Capstone SENG499 class: Company 2 Course Scheduler Project. 
Authored by the Company2-Algorithm1 sub-team.

## Install from PyPi Using PIP
Install this package into your environment from PyPi using `pip`. 

```bash
$ pip install coursescheduler==0.0.1
```
The most recent available version of the package is uploaded to the test PyPi index automatically.
To ensure that you are working with the most recent release upgrade this module before integrating.

```bash
$ python3 -m pip install --upgrade coursescheduler
```

## Install from Local Archives

Clone this repo into your repository. Inside the algorithm 1 module directory,
build and install the package as shown below. 

```bash
$ python3 -m build
$ pip3 install coursescheduler-0.0.1.tar.gz
```

## Usage
The algorithm 1 module may then be imported into and called from the backend subteam. In the example below
`historical_course_data` `professors` and `schedule` are python dictionaries or
JSON strings. A schedule object with capacities assigned is encoded as a JSON string and returned
to caller.

```python
from coursescheduler.scheduler import generate_schedule
schedule = generate_schedule(historical_course_data, professors, schedule)
```

## Dev 

To make and test changes to the project, navigate into the root level directory 
`/path/to/algorithm1/`. After editing the projet files, in order for the changes to take
effect you must reinstall the local package by the following cmd:

```bash
$ pip3 install . 
```

To run the tests

```bash
$ cd tests
$ python -m pytest
```
