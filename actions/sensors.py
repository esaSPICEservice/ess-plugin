import cosmoscripting
from utils.generators import SENSOR_SUFFIX
from ui.common import get_runtime
import json


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

def get_sensor_names():
    sensors = get_sensors()
    sensor_names = {}
    for key in sensors:
        sensor_names[key] = [ sensor.get('name') for sensor in sensors[key]]
    return sensor_names

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


def reconfigure_sensors(show_frustum, state):
    run_time = get_runtime()
    sensors_file_path = run_time.get('sensors_file_path')
    if sensors_file_path:
        cosmo = cosmoscripting.Cosmo()
        with open(sensors_file_path, 'r') as sensors_file:
            sensors_json = json.load(sensors_file)

        items = sensors_json.get('items')
        for item in items:
            item['geometry']['frustumOpacity'] = 0.8 if show_frustum else 0

        with open(sensors_file_path, 'w') as sensors_file:
            json.dump(sensors_json, sensors_file, indent=2)
        
        # temporary solution - we shall garantee that the last
        # catalog is the sensor

        cosmo.unloadLastCatalog()
        cosmo.loadCatalogFile(sensors_file_path)

        # Reset sensor status
        for name, state in state.items():
            toggle_sensor(state, name)