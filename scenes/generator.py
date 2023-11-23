import os
import json
from actions.sensors import get_sensor_list
from utils.generators import Sensor, SensorGenerator

from datetime import datetime

TIMESTAMP_FORMAT = '%Y%m%dT%H%M%S%f'

data_folder = os.path.join(os.path.dirname(__file__), 'data', 'juice')

def generate_sensor(name, parent_path):
    generator = SensorGenerator(
        Sensor(
                name, 'Jupiter', 
                [0, 0.6, 0], None),
        'JUICE')
    generator.save(os.path.abspath(os.path.join(parent_path, f"{name}.json")))
    return f'./sensors/{name}.json'

def create_cosmo_scene(parent_path, metakernel, extra):

    scene_json = {
        "version": "1.0",
        "name": "ESS-Plugin Scene",
        "require": [
                "./spice.json",
                f"{data_folder}/spacecraft_JUICE_arcs.json",
                f"{data_folder}/spacecraft_JUICE_MGA_arcs.json",
                f"{data_folder}/spacecraft_JUICE_SOLAR_ARRAYS_arcs.json",
                f"{data_folder}/jupiter_minor_moons_ananke_group.json",
                f"{data_folder}/jupiter_minor_moons_carme_group.json",
                f"{data_folder}/jupiter_minor_moons_inner_group.json",
                f"{data_folder}/jupiter_minor_moons_pasiphae_group.json",
                f"{data_folder}/jupiter_minor_moons_prograde_groups.json",
                f"{data_folder}/jupiter_rings.json",
                f"{data_folder}/moon_torus.json"
            ]
    }

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