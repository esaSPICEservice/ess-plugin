import os
from .utils import create_structure
from simulator.osve import osve
from scenes.generator import create_cosmo_scene, generate_working_dir


def simulate(meta_kernel, ptr_content, no_power, no_sa, no_mga, step=5):
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
                                         no_sa=no_sa,
                                         no_mga=no_mga,
                                         quaternions=False)

    root_scenario_path = os.path.dirname(session_file_path)
    status_code = sim.execute(root_scenario_path, session_file_path)

    if status_code == 0:
        mk = "./kernel/" + os.path.basename(meta_kernel)
        extra = []
        cks = ['juice_sc_ptr.bc', 'juice_sa_ptr.bc', 'juice_mga_ptr.bc']
        for ck in cks:
            if os.path.exists(os.path.join(root_scenario_path, 'output', ck)):
                extra.append("./output/" + ck)

        return True, create_cosmo_scene(root_scenario_path, mk, extra), root_scenario_path
    else:
        return False, os.path.join(root_scenario_path, 'output', 'log.json'), root_scenario_path