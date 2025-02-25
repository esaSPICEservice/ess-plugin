import os
import json
from actions.sensors import get_sensor_list
from utils.generators import Sensor, SensorGenerator, CustomStarsGenerator
from ui.common import get_runtime, get_settings
import cosmoscripting

from datetime import datetime

TIMESTAMP_FORMAT = '%Y%m%dT%H%M%S%f'


def generate_all_sensor(sensor_list, parent_path):

    run_time = get_runtime()
    generator = SensorGenerator()
    for sensor in sensor_list:
        instrument = sensor.get('name')
        color = sensor.get('color')
        sc = sensor.get('spacecraft', run_time.get('spacecraft', ''))
        sensor = Sensor(
                instrument, run_time.get('central_body', ''), 
                color, None)
       
        generator.append(sensor, sc)

    file_path = os.path.abspath(os.path.join(parent_path, "sensors.json"))
    generator.save(file_path)
    run_time.set('sensors_file_path', file_path)
    return file_path

def generate_custom_stars(parent_path):
    filename = "custom_stars.json"
    run_time = get_runtime()
    spacecraft = run_time.get('spacecraft', '')
    settings = get_settings()
    generator = CustomStarsGenerator()
    for star in settings.get('stardb', 'star_list', []):
        generator.append(star.get('ra'), star.get('dec'), star.get('name'), spacecraft)

    file_path = os.path.abspath(os.path.join(parent_path, filename))
    generator.save(file_path)
    return filename


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

    # Custom stars added
    custom_star_filename = generate_custom_stars(parent_path)
    scene_json.get('require').append(custom_star_filename)

    all_sensor_path = generate_all_sensor(get_sensor_list(), parent_path)

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

    return scene_file_path, all_sensor_path


def timestamp():
    return datetime.now().strftime(TIMESTAMP_FORMAT)


def generate_working_dir():
    working_dir = os.path.join(os.path.dirname(__file__), '..', 'tmp', timestamp())
    os.makedirs(working_dir)
    return working_dir