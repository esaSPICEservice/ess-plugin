import cosmoscripting
from utils.generators import SENSOR_SUFFIX, SENSOR_FRUSTUM_ON_OPACITY
from ui.common import get_runtime
from utils.generators import append_observation
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

def get_targets():
    runtime = get_runtime()
    sensors = runtime.get('targets')
    return sensors

def get_sensor(name):
    sensors = get_sensors()
    for key in sensors:
        for sensor in sensors[key]:
            if sensor.get('name') == name:
                return sensor
    return None


def get_sensor_names():
    sensors = get_sensors()
    sensor_names = {}
    for key in sensors:
        sensor_names[key] = [ sensor.get('name') for sensor in sensors[key]]
    return sensor_names

def get_sensor_ids():
    sensors = get_sensors()
    sensor_names = []
    for key in sensors:
        sensor_names.extend([sensor.get('name') for sensor in sensors[key]])
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

def hide_sensor(sensor_id):
    cosmo = cosmoscripting.Cosmo()
    cosmo.hideObject(sensor_id)


def reconfigure_catalogue():
    run_time = get_runtime()

    sensors_file_path = run_time.get('sensors_file_path')
    state = run_time.get('sensors_state')
    

    
    if sensors_file_path:
        cosmo = cosmoscripting.Cosmo()
        with open(sensors_file_path, 'r') as sensors_file:
            sensors_json = json.load(sensors_file)

        items, current_sensors = reconfigure_sensors(sensors_json.get('items'))
        
        # We remove the observations in this step
        sensors_json['items'] = items

        # And we setup them from scratch
        reconfigure_observations(sensors_json.get('items'))

        with open(sensors_file_path, 'w') as sensors_file:
            json.dump(sensors_json, sensors_file, indent=2)
        
        # temporary solution - we shall garantee that the last
        # catalog is the sensor

        cosmo.unloadLastCatalog()
        cosmo.loadCatalogFile(sensors_file_path)

        # Reset sensor status
        if state is not None:
            for name, state in state.items():
                toggle_sensor(state, name)
        else:
            for sensor_id in current_sensors:
                hide_sensor(sensor_id)


def reconfigure_sensors(items):
    run_time = get_runtime()
    show_frustum = run_time.get('sensors_frustrum', False)
    current_sensors = []
    sensors = []
    for item in items:
        if item['class'] == 'sensor':
            item['geometry']['frustumOpacity'] = SENSOR_FRUSTUM_ON_OPACITY if show_frustum else 0
            current_sensors.append(item['name'])
            sensors.append(item)
    return sensors, current_sensors


def reconfigure_observations(items):
    run_time = get_runtime()
    observations = run_time.get('observations', [])
    for index, observation in enumerate(observations):
        sensor_name = observation[0]
        sensor_id = sensor_name + '_SENSOR'
        sensor = get_sensor(sensor_name)
        color = [0, 0, 1]
        if sensor is not None:
            color = sensor.get('color')
        append_observation(items, index, observation[1], sensor_id , observation[2][:-1] + ' UTC', observation[3][:-1] + ' UTC', color)