# Powergrid (prototype)

Powergrid is an open source power management application for Linux laptops designed to automatically adjust power
settings to extend battery life and reduce power consumption. It is user-friendly, lightweight, and offers a range of
customizable options to meet various needs.

The aplication is designed to work with various Linux distributions but it was tested only with OpenSuse, Ubuntu, KDE Neon and Manjaro.

The development of Powergrid was influenced by Powertop, and its optimization results were compared against those of
Powertop. On the hardware it was tested on, Powergrid performed as well as, or better than, Powertop.

### How it works

Powergrid relies on the Linux device manager udev that dynamically creates and manages device nodes in the /dev directory. When a device is added or removed from the system, udev receives an event and triggers an action.

#### Here's how udev works:

* Kernel sends an event: When a device is connected or disconnected from the system, the kernel sends an event to udev.

* udev rules match: The udev daemon checks the rules configured in the system for device handling. These rules can be found in /etc/udev/rules.d/ directory.

* Attributes for the device are collected: udev collects attributes of the device, such as its name, vendor ID, product ID, etc. from the kernel.

* udev creates or modifies a device node: Based on the collected attributes and rules, udev creates or modifies a device node in the /dev directory. This device node is then used to communicate with the device.

* Other services are notified: After creating or modifying a device node, udev sends a message to other system services, such as the graphical user interface, to update the device list.


Powergrid generates rules for power_supply device change events that run a shell script to optimize power consumption for devices which support power management. 

#### An example of such a rule is provided below.

* An example of the rule for the AC power adapter is connected

`SUBSYSTEM=="power_supply", ACTION=="change", ATTR{online}=="1", RUN+=""`

* An example of the rule for the AC power adapter is disconnected

`SUBSYSTEM=="power_supply", ACTION=="change", ATTR{online}=="0", RUN+=""`


The script to be run will be placed inside the RUN+="" element. For example, let's say the optimization script looks like this: 

`echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor`. 

The resulting udev rule will look like:

`SUBSYSTEM=="power_supply", ACTION=="change", ATTR{online}=="1", RUN+="echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"`


The Powergrid scans the `/dev` directory for devices that support power management and generates a long list of rules. You can investigate these rules in the 'Udev rules' tab. Once you press the 'Apply' button, Powergrid installs the generated rules inside `/etc/udev/rules.d/70-performance.rules`.

Additionally, you can export all the rules into a text file.






### How to run

Download the AppImage from the releases page:

[Powergrid.AppImage](https://github.com/AlexWoroschilow/Powergrid.AppImage/releases)

`wget https://github.com/AlexWoroschilow/Powergrid.AppImage/releases/download/latest/Powergrid.AppImage`

grant the execution permissions:

`chmod +x Powergrid.AppImage`

run the downloaded AppImage:

`./Powergrid.AppImage`



# Screenshots

![Dashboard](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/dashboard.png?raw=true)
![CPU](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-cpu.png?raw=true)
![Discs](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-sata.png?raw=true)
![USB](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-usb.png?raw=true)
![PCI](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-pci.png?raw=true)
![HDA](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-hda.png?raw=true)
![I2C](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-i2c.png?raw=true)
![SCSI](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/devices-scsi.png?raw=true)
![Udev](https://github.com/AlexWoroschilow/Powergrid.AppImage/blob/main/screenshots/udev-rules.png?raw=true)
