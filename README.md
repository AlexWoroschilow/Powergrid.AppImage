# Performance Tuner
is a free open source program for the energy consumption fine-tuning in Linux, inspired by the powertop, and tlp. You can setup the performance schema using the gui and apply the stup to the system. 

The program will generate folowing files:
* `/etc/udev/rules.d/70-performance.rules`
* `/etc/performance-tuner/performance_*`
* `/etc/performance-tuner/powersave_*`

According to the power source (AC or Battery) the `/etc/performance-tuner/performance_*` or `/etc/performance-tuner/powersave_` will be started by the udev. 




### How to run
To be able to run the programm you will need the python3 and python3-virtualenv installed

Activate python virtual environment:
`source venv/bin/activate`

Install required modules:
`python3 -m pip install -r ./requirements.txt`

Run the programm:
`python3 -m fbs run`

### How to build an AppImage

To be able to run the programm you will need the python3 (3.7) and python3-virtualenv installed.

Install required modules:
`python3 -m pip install -r ./requirements.txt`

Build appimage:
`make`

Run the program:
`bin/AOD-PerformanceTuner.AppImage`



![Dashboard](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/dashboard.png?raw=true)

![Device management](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices.png?raw=true)

