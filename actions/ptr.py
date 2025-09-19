import os
from actions.common import add_juice_menu
from actions.time_navigation import goto_date
import cosmoscripting
from simulator.wrapper import simulate
from ui.blocks_ui import BlocksDialog
from ui.navigation_ui import NavigationDialog
from simulator.osve.utils import get_platform
my_platform = get_platform()
if (my_platform.startswith("windows")):
    from utils.re_block_parser import BlockParser
else:
    from utils.block_parser import BlockParser
import json

from PyQt5.QtWidgets import QMessageBox

from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec, get_catalog_handler
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog
from ui.power_ui import PowerDialog


def dump_error(log_path):
    with open(log_path, 'r') as log_file:
            log_json = json.load(log_file)
    errors =  list(filter(lambda entry: entry.get('severity', 'INFO') == 'ERROR', log_json))
    raise ValueError(json.dumps(errors, indent=2))


def execute_ptr(mk, content, calculate_power, calculate_sa, calculate_mga):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    success, catalog, sensor_catalog, root_scenario = simulate(
        mk, content, 
        not calculate_power, not calculate_sa, not calculate_mga)
    if success:
        handler = get_catalog_handler()
        handler.add_catalog(catalog)
        handler.add_catalog(sensor_catalog)
        after_load(root_scenario)
        goto_date(start_time + ' UTC')
    else:
        dump_error(catalog)



def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]

def after_load(root_scenario):
    main_window = get_main_window()

    resolved_ptr = os.path.join(root_scenario, 'output', 'ptr_resolved.ptx')
    power_file  = os.path.join(root_scenario, 'output', 'power.csv')
    
    menu = []

    if not my_platform.startswith("windows"):
        if os.path.exists(resolved_ptr):
            bp = BlocksDialog(main_window, resolved_ptr)
            menu.append(
                ActionSpec('Blocks', 'Show pointing blocks', '', bp.show_and_focus)
            )
            bp.show_and_focus()

    if os.path.exists(power_file) and not my_platform.startswith("windows"):
            pw = PowerDialog(main_window, power_file)
            menu.append(
                ActionSpec('SA Produced power', 'Solar Array produced power', '', pw.show_and_focus)
            )

    add_menu(main_window, MenuSpec('Pointing', menu))

    add_juice_menu()



