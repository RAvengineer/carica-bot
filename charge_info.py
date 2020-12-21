from platform import system as ps
import subprocess

commands = {
    'Linux': ['cat','/sys/class/power_supply/BAT0/capacity'],
    'Windows': ['WMIC', 'PATH', 'Win32_Battery', 'Get', 'EstimatedChargeRemaining'],
}

def readBattery():
    # TODO: Add docstring
    read_battery_command = commands.get(ps(), 'NA')
    if(read_battery_command == 'NA'):
        return -1 # TODO: Raise exception here
    # TODO: Use Try/Except here
    battery_percentage = subprocess.run(read_battery_command, stdout=subprocess.PIPE, text=True,)
    battery_percentage = (int)(battery_percentage.stdout[:-1])
    print(battery_percentage)

readBattery()

"""
References:
    -   [Get Platform information - w3resource]
        (https://www.w3resource.com/python-exercises/python-basic-exercise-43.php?passed=passed)
    -   [Executing Shell commands in Python]
        (https://stackabuse.com/executing-shell-commands-with-python/)
    -   [Python - How to call an external command? - Stack Overflow]
        (https://stackoverflow.com/questions/89228/how-to-call-an-external-command)
    -   [How to check Battery level via Command line | Scott Larson]
        (http://www.scottrlarson.com/updates/update-battery-life-via-cmd-line/)

"""