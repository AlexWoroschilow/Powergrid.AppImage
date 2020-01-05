# PerformanceTuner
is a free open source program for the energy consumption fine-tuning in Linux, inspired by the powertop, and tlp.

# How to run
To be able to run the programm you will need the python3 and python3-virtualenv installed

Activate python virtual environment:
`source venv/bin/activate`

Install required modules:
`python3 -m pip install -r ./requirements.txt`

Run the programm:
`python3 -m fbs run`

# How to build AppImage

To be able to run the programm you will need the python3 (3.7) and python3-virtualenv installed.

Activate python virtual environment:
`source venv/bin/activate`

Install required modules:
`python3 -m pip install -r ./requirements.txt`

Build appimage:
`make`

Run the program:
`bin/AOD-PerformanceTuner.AppImage`



![alt text](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/dashboard.png?raw=true)
