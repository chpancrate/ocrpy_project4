# Project 4 of the OpenClassRoom Python developper training 

## Summary
This project is a script used to manage Chess Tournaments.

The interface used is the command line.

The data are stored in JSON files placed in the directory ./data
The reports are produced in the directory ./rapports

## Requirements
These scripts run with Python 3.11.1.

To install python you can download it here : https://www.python.org/downloads/

If you are new to Python you can find information here : https://www.python.org/about/gettingstarted/ 

It is better to run the scripts in a virtual environment. You can find information on virtual envrionments here : https://docs.python.org/3/library/venv.html 

Once in your virtual environment, the following module need to be installed :
- prettytable : 3.6.0
- flake8      : 6.0.0
- flake8-html : 0.4.3

All the modules needed for the scripts are in requirements.txt. A quick way to install them is to run the command below in a python terminal:
```
pip install -r requirements.txt
```

## How to run the application

In order to run the script, clone the following repository in the directory where you want the data to be stored : https://github.com/chpancrate/ocrpy_project4

Then use the command : 
```
python ./main.py
```
The script will show the menus needed to interract with it.
It will create all the needed files and directories.

## How to run the flake8 report

Ensure the you have installed flake8 and flake8-html as described in the requirements section.
In the directory where the main.py is located, run the following command :
```
flake8 --exclude=ENVDIR --format=html --htmldir=flake-report 
``` 
where ENVDIR is the configuration directory of your virtual environment, example :
```
flake8 --exclude=.env --format=html --htmldir=flake-report 
``` 
The result can be accessed by opening the index.html file in the flake-report directory.
