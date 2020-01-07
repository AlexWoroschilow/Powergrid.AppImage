# Performance Tuner (prototype)
The performance tuner is a free open source program for the energy consumption fine-tuning in Linux, inspired by the powertop, and tlp. You can setup the performance schema using the gui and apply the setup to the system. 

The program will generate folowing files:
* `/etc/udev/rules.d/70-performance.rules`
* `/etc/performance-tuner/performance_*`
* `/etc/performance-tuner/powersave_*`

According to the power source (AC or Battery) the `/etc/performance-tuner/performance_*` or `/etc/performance-tuner/powersave_` scripts will be started by the udev. 


This is a fully functional prototype and MVP how i see it.

You use it at your own risk still any feedback will be highly appreciated.



### How to run
To be able to run the programm you will need the python3 and python3-virtualenv installed

Install required modules:
`make init`

Activate python virtual environment:
`source venv/bin/activate`

Run the programm:
`python3 src/main.py`

### How to build an AppImage

To be able to run the programm you will need the python3 (3.7) and python3-virtualenv installed.

Build appimage:
`make`

Run the program:
`bin/AOD-PerformanceTuner.AppImage`



![Dashboard](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/dashboard.png?raw=true)

![Device management](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices.png?raw=true)

