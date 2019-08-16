Developer Notes 
================

## Ease of developement

To make developing easier add the DARNprocessing path to your 
    PYTHONPATH
This will use the currently used code in an import statement instead of 
reinstalling the setup.py 

Before pushing always test with 
    sudo python setup.py install
to ensure the install procedure still works. 

## Programming Practices

### Programming Style Practices

The following programming principles must be followed:
    - PEP 8 style https://www.python.org/dev/peps/pep-0008/?
    - python 3
    - docstring 

### Programming Code Practices 

The following must be included:
    - unit test cases
    - documentation on use cases for other users
    -

## Pull Request procedures

Each pull request should include:
    - code review 
    - testing with unit tests and user tests 

## Pydarn releses

Releases follow this manner:
    - minor releases "patches" x.x.x+1
        - bug fixes 
        - minor changes like adding extra exceptions
    - minor-major releases x.x+1.0
        - default changes 
        - major bug fixes 
        - small algorithm changes or updates 
    - major releases x+1.0.0
        - new features 
        - new algorithms 
        - new visuals 


