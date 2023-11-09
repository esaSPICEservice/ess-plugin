"""PTR Command Line Interface module."""
import os

from .utils import create_structure
from .utils import timestamp

from simulator.osve import osve

def execute(root_scenario_path, session_file_path):
    sim = osve.osve()
    sim.execute(root_scenario_path, session_file_path)


def test(meta_kernel, ptr_content):
    the_osve = osve.osve()
    print("")
    print("OSVE LIB VERSION:       ", the_osve.get_app_version())
    print("OSVE AGM VERSION:       ", the_osve.get_agm_version())
    print("OSVE EPS VERSION:       ", the_osve.get_eps_version())
    print("")
    

    working_dir = os.path.join(os.path.dirname(__file__), timestamp())
    os.makedirs(working_dir)
    session_file_path = create_structure(working_dir, meta_kernel, ptr_content,
                                         step=5,
                                         no_power=False,
                                         quaternions=False)
    root_scenario_path = os.path.dirname(session_file_path)

    print("ptwrapper session execution")

    execute(root_scenario_path, session_file_path)

    return os.path.abspath(os.path.join(root_scenario_path, "scene.json"))