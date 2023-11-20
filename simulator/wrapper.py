"""PTR Command Line Interface module."""
import os
import json
from .utils import create_structure
from .utils import timestamp
from utils.generators import Sensor, SensorGenerator
from simulator.osve import osve

def generate_sensor(name, parent_path):
    generator = SensorGenerator(
        Sensor(
                name, 'Jupiter', 
                [0, 0.6, 0], None),
        'JUICE')
    generator.save(os.path.abspath(os.path.join(parent_path, f"{name}.json")))
    return f'./sensors/{name}.json'

def create_cosmo_scene(parent_path, metakernel):

    scene_json = {
        "version": "1.0",
        "name": "ESS-Plugin Scene",
        "require": [
                "./spice.json",
                "../config/cosmo/spacecraft_JUICE_arcs.json",
                "../config/cosmo/spacecraft_JUICE_MGA_arcs.json",
                "../config/cosmo/spacecraft_JUICE_SOLAR_ARRAYS_arcs.json",
                "../config/cosmo/jupiter_minor_moons_ananke_group.json",
                "../config/cosmo/jupiter_minor_moons_carme_group.json",
                "../config/cosmo/jupiter_minor_moons_inner_group.json",
                "../config/cosmo/jupiter_minor_moons_pasiphae_group.json",
                "../config/cosmo/jupiter_minor_moons_prograde_groups.json",
                "../config/cosmo/jupiter_rings.json",
                "../config/cosmo/moon_torus.json"
            ]
    }

    sensor_folder = os.path.join(parent_path, 'sensors')
    os.makedirs(sensor_folder)
    for instrument in ['JUICE_JANUS']:
        scene_json.get('require').append(generate_sensor(instrument, sensor_folder))

    scene_file_path = os.path.abspath(os.path.join(parent_path, "scene.json"))
    with open(scene_file_path, "w") as scene_json_file:
        json.dump(scene_json, scene_json_file, indent=2)


    spice_json = {
        "version": "1.0",
        "name": "ESS-Plugin Kernel",
        "spiceKernels": [
        "./kernel/" + os.path.basename(metakernel),
        "./output/juice_sc_ptr.bc"
        ]
    }

    spice_file_path = os.path.abspath(os.path.join(parent_path, "spice.json"))
    with open(spice_file_path, "w") as spice_json_file:
        json.dump(spice_json, spice_json_file, indent=2)

    return scene_file_path

def simulate(meta_kernel, ptr_content, no_power, step=5):
    sim = osve.osve()
    
    print("")
    print("OSVE LIB VERSION:       ", sim.get_app_version())
    print("OSVE AGM VERSION:       ", sim.get_agm_version())
    print("OSVE EPS VERSION:       ", sim.get_eps_version())
    print("")

    working_dir = os.path.join(os.path.dirname(__file__), timestamp())
    os.makedirs(working_dir)
    session_file_path = create_structure(working_dir, meta_kernel, ptr_content,
                                         step=step,
                                         no_power=no_power,
                                         quaternions=False)

    root_scenario_path = os.path.dirname(session_file_path)
    status_code = sim.execute(root_scenario_path, session_file_path)

    if status_code == 0:
        return True, create_cosmo_scene(root_scenario_path, meta_kernel), root_scenario_path
    else:
        return False, os.path.join(root_scenario_path, 'output', 'log.json'), root_scenario_path