# Control fan on RockPro64 according to CPU temperature

This is a simple python script that I use to control fan on RockPro64 SBC running Armbian + OpenMediaVault. All it does is reading temperature from armbianmonitor, converting it to PWM duty on dedicated FAN connector and writing it to hwmon, enabling or disabling the fan.

## Parameters to configure
``FAN_PWM_LOW`` is a PWM duty when fan actually starts to spin. It may differ for each part, but in my case it was around 200. 
``FAN_PWM_HIGH`` is a maximum PWM duty that can be written to hwmon. Should be just set to 255.
``TEMPERATURE_LOW`` is a temperature level below which fan stops to spin. Set is according to your needs.
``TEMPERATURE_HIGH`` is a temperature threshold over which fan spins with 100% speed.
Between ``TEMPERATURE_LOW`` and ``TEMPERATURE_HIGH`` fan speed is linearly interpolated from current temperature.
## Run on startup
There are many ways to start a script on boot in Linux. I just added it to crontab in OpenMediaVault GUI setting execution time to **on boot** and specifying command as ``python3 <path to script> fan_controller``.

Before running it from cron I recommend testing it in command line to make sure that everything actually works.

## Dealing with changing hwmon name

Actual name of hwmon differs between reboots. Sometimes it is called hwmon2, the other time hwmon3. In this system there is only one hwmon anyway, so number is found by polling each name in certain range. This is not elegant solution and will break if more hwmons are found in a system.

