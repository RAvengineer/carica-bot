from psutil import sensors_battery as battery

commands = {
    'Linux': ['cat','/sys/class/power_supply/BAT0/capacity'],
    'Windows': ['WMIC', 'PATH', 'Win32_Battery', 'Get', 'EstimatedChargeRemaining'],
}

def readBattery():
    # TODO: Add docstring
    try:
        battery_status = battery()
        if(battery_status == None):
            raise Exception("Battery NOT FOUND!")
        battery_percentage = (int)(battery_status.percent)
        print(battery_percentage)
    except Exception as e:
        raise Exception(f'Error in charge_info.py:readBattery: {str(e)}')

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
    -   [Python script to shows Laptop Battery Percentage - GeeksforGeeks]
        (https://www.geeksforgeeks.org/python-script-to-shows-laptop-battery-percentage/)
    -   [psutil - PyPI](https://pypi.org/project/psutil/)

"""