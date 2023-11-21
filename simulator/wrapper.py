import os
from .utils import create_structure
from simulator.osve import osve
from scenes.generator import create_cosmo_scene, generate_working_dir


def simulate(meta_kernel, ptr_content, no_power, step=5):
    sim = osve.osve()
    
    print("")
    print("OSVE LIB VERSION:       ", sim.get_app_version())
    print("OSVE AGM VERSION:       ", sim.get_agm_version())
    print("OSVE EPS VERSION:       ", sim.get_eps_version())
    print("")

    working_dir = generate_working_dir()

    session_file_path = create_structure(working_dir, meta_kernel, ptr_content,
                                         step=step,
                                         no_power=no_power,
                                         quaternions=False)

    root_scenario_path = os.path.dirname(session_file_path)
    status_code = sim.execute(root_scenario_path, session_file_path)

    if status_code == 0:
        mk = "./kernel/" + os.path.basename(meta_kernel)
        extra = ["./output/juice_sc_ptr.bc"]
        return True, create_cosmo_scene(root_scenario_path, mk, extra), root_scenario_path
    else:
        return False, os.path.join(root_scenario_path, 'output', 'log.json'), root_scenario_path