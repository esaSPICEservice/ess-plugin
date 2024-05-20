import cosmoscripting
from utils.generators import SENSOR_SUFFIX
from ui.common import get_runtime


def get_sensor_list():
    sensor_list = []
    sensors = get_sensors()
    for instrument in sensors:
        sensor_list.extend(sensors[instrument])
    return sensor_list


def get_sensors():
    runtime = get_runtime()
    sensors = runtime.get('sensors')
    return sensors


def get_boresights():
    runtime = get_runtime()
    boresights = runtime.get('boresights')
    return boresights


def toggle_sensor(visible, name):
    cosmo = cosmoscripting.Cosmo()
    sensor_id = name + SENSOR_SUFFIX
    if visible:
        cosmo.showObject(sensor_id)
    else:
        cosmo.hideObject(sensor_id)
