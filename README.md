# Powergrid (prototype)

Powergrid is an open source power management application for Linux laptops designed to automatically adjust power settings to extend battery life and reduce power consumption. It is user-friendly, lightweight, and offers a range of customizable options to meet various needs.

Powergrid is designed to work with various Linux distributions, including OpenSuse, Ubuntu, and Manjaro, among others.

The application creates udev rules that execute commands to optimize power consumption based on AC/Battery events. After the rules have been applied, Powergrid terminates and the udev subsystem continues to maintain the optimizations.

The development of Powergrid was influenced by Powertop, and its optimization results were compared against those of Powertop. On the hardware it was tested on, Powergrid performed as well as, or better than, Powertop.


# Screenshots
![Dashboard](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/dashboard.png?raw=true)
![CPU](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-cpu.png?raw=true)
![Discs](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-sata.png?raw=true)
![USB](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-usb.png?raw=true)
![PCI](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-pci.png?raw=true)
![HDA](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-hda.png?raw=true)
![I2C](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-i2c.png?raw=true)
![SCSI](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-scsi.png?raw=true)
![Udev](https://github.com/AlexWoroschilow/AOD-PerformanceTuner/blob/master/screenshots/devices-udev.png?raw=true)

### How to run

Download the AppImage from the releases page: 

[Powergrid.AppImage](https://github.com/AlexWoroschilow/PerformanceTuner.AppImage/releases)

`wget https://github.com/AlexWoroschilow/PerformanceTuner.AppImage/releases/download/latest/PerformanceTuner.AppImage`

grant the execution permissions:

`chmod +x Powergrid.AppImage`

run the downloaded AppImage:

`./Powergrid.AppImage`
