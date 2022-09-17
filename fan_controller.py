#!/usr/bin/env python

import time
import os

FAN_PWM_LOW = 200
FAN_PWM_HIGH = 255

TEMPERATURE_LOW = 60    #below this temperature fan does not spin
TEMPERATURE_HIGH = 85   #over this temperature fan spins with 100% speed

# Write PWM duty to file in existing hwmon
def setFanSpeedRAW(speed): 
    speed = int(speed)  #convert speed to integer (required by hwmon)

    for hwmon_id in range(16):
        if os.path.exists("/sys/devices/platform/pwm-fan/hwmon/hwmon" + str(hwmon_id) + "/pwm1"):
            with open("/sys/devices/platform/pwm-fan/hwmon/hwmon" + str(hwmon_id) + "/pwm1", "w") as fhandle:
                print("hmnon found as hwmon", str(hwmon_id))
                fhandle.write(str(speed))
    print("setFanSpeedRAW = ", str(speed))
    

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def setFanSpeedPercent(speed):
    if speed == 0:
        setFanSpeedRAW(0);
        return
    speed = map(speed, 0, 100, FAN_PWM_LOW, FAN_PWM_HIGH)
    setFanSpeedRAW(speed)
    

def getTemperature():
    with open('/etc/armbianmonitor/datasources/soctemp', 'r') as fhandle:
        temp = int(fhandle.read())/1000
        return round(temp, 1)


# main script

print("Fan turn off temperature threshold =   ", TEMPERATURE_LOW)
print("Fan full speed temperature threshold = ", TEMPERATURE_HIGH)
print(" ")

# infinite loop
while 1:
    temp = getTemperature()

    if temp < TEMPERATURE_LOW:
        setFanSpeedPercent(0)

    elif temp > TEMPERATURE_HIGH:
        setFanSpeedPercent(100)
    
    else:
        speed = map(temp, TEMPERATURE_LOW, TEMPERATURE_HIGH, 0, 100)
        setFanSpeedPercent(speed);

    print("CPU temperature = ", temp, "C")
    time.sleep(5)

