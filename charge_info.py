"""Utilities for processing & analyzing battery details"""

from plyer import notification, battery
from os import getcwd, getenv
from yaml import safe_load, safe_dump

def readBattery() -> dict:
    # TODO: Add docstring
    try:
        # Read battery status in the form {'isCharging': False, 'percentage': 69.0}
        battery_status = battery.status # dict
        if(battery_status['percentage'] == None):
            raise Exception("Battery NOT FOUND!")
        return battery_status
    except Exception as e:
        raise Exception(f'Error in charge_info.py:readBattery - {str(e)}')

def notify(message):
    """Send a notification to the user machine

    Parameters
    ----------
    - message : `str`
        - The message to be displayed in the notification

    Raises
    ------
    - Exception
        - Custom Exception
    """
    # TODO: Change Exception desc in Docstring
    try:
        notification.notify(
            title='Carica Bot',
            message=message,
            app_name='Carica Bot',
            app_icon=f'{getcwd()}/carica_bot_logo.jpg',
            timeout=60,
        )
    except Exception as e:
        raise Exception(f'Error in charge_info.py:notify - {str(e)}')

def checkBattery():
    try:
        battery_status: dict = readBattery()
        percent, is_charging = battery_status['percentage'], battery_status['isCharging']

        # Read the battery prefs from the prefs.yaml
        # The values are read in this function, coz if the prefs are modified by a 
        # different function, this function will be always read
        # the modified value as this function will be called periodically.
        with open(getenv('BOT_PREFS')) as prefs:
            battery_percent: dict = safe_load(prefs)['battery-percent']
            max_percent = battery_percent['max']
            min_percent = battery_percent['min']

    except Exception as e:
        # TODO: Convert print to logs
        print(f'Exception in charge_info:checkBattery()\n{str(e)}')


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
    -   [Plyer documentation](https://plyer.readthedocs.io/en/latest/)
    -   [dbus warning in plyer - Stack Overflow](https://stackoverflow.com/a/54072196)

"""