import os
import json
from actions.sensors import get_sensor_list
from utils.generators import Sensor, SensorGenerator
from ui.common import get_runtime

from datetime import datetime

TIMESTAMP_FORMAT = '%Y%m%dT%H%M%S%f'



def generate_sensor(name, parent_path):

    run_time = get_runtime()

    generator = SensorGenerator(
        Sensor(
                name, run_time.get('central_body', ''), 
                [0, 0.6, 0], None),
        run_time.get('spacecraft', ''))
    generator.save(os.path.abspath(os.path.join(parent_path, "{name}.json".format(name=name))))
    return './sensors/'+ name + '.json'



def create_cosmo_scene(parent_path, metakernel, extra):


    run_time = get_runtime()
    data_folder = os.path.join(os.path.dirname(__file__), 'data',  run_time.get('spacecraft', '').lower())

    scene_json = {
        "version": "1.0",
        "name": "ESS-Plugin Scene",
        "require": [
                "./spice.json",
            ]
    }

    for model in run_time.get('models', []):
        scene_json.get('require').append("{data_folder}/{model}".format(data_folder=data_folder,model=model))


    sensor_folder = os.path.join(parent_path, 'sensors')
    os.makedirs(sensor_folder)
    for instrument in get_sensor_list():
        scene_json.get('require').append(generate_sensor(instrument, sensor_folder))

    scene_file_path = os.path.abspath(os.path.join(parent_path, "scene.json"))
    with open(scene_file_path, "w") as scene_json_file:
        json.dump(scene_json, scene_json_file, indent=2)


    spice_json = {
        "version": "1.0",
        "name": "ESS-Plugin Kernel",
        "spiceKernels": [
            metakernel
        ]
    }
    spice_json.get('spiceKernels').extend(extra)

    spice_file_path = os.path.abspath(os.path.join(parent_path, "spice.json"))
    with open(spice_file_path, "w") as spice_json_file:
        json.dump(spice_json, spice_json_file, indent=2)

    return scene_file_path


def timestamp():
    return datetime.now().strftime(TIMESTAMP_FORMAT)


def generate_working_dir():
    working_dir = os.path.join(os.path.dirname(__file__), '..', 'tmp', timestamp())
    os.makedirs(working_dir)
    return working_dir