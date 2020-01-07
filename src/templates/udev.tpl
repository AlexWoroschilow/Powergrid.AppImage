SUBSYSTEM=="power_supply", ACTION=="change", ATTR{online}=="1", RUN+="$performance"
SUBSYSTEM=="power_supply", ACTION=="change", ATTR{online}=="0", RUN+="$powersave"
