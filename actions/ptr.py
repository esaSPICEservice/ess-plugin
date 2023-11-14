import os
from actions.time_navigation import goto_date
import cosmoscripting
from simulator.wrapper import simulate
from ui.blocks_ui import BlocksDialog
from utils.block_parser import BlockParser

from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog
from ui.power_ui import PowerDialog

def execute_ptr(mk, content, calculate_power):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    catalog, root_scenario = simulate(mk, content, not calculate_power)
    cosmo.loadCatalogFile(catalog)
    after_load(root_scenario)
    goto_date(start_time + ' UTC')


def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]

def after_load(root_scenario):
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)


    resolved_ptr = os.path.join(root_scenario, 'output', 'ptr_resolved.ptx')
    power_file  = os.path.join(root_scenario, 'output', 'power.csv')
    
    menu = []

    if os.path.exists(resolved_ptr):
        bp = BlocksDialog(main_window, resolved_ptr)
        menu.append(
            ActionSpec('Blocks', 'Show pointing blocks', '', bp.show_and_focus)
        )

    if os.path.exists(power_file):
        pw = PowerDialog(main_window, power_file)
        menu.append(
            ActionSpec('SA Produced power', 'Solar Array produced power', '', pw.show_and_focus)
        )

    add_menu(main_window, MenuSpec('Pointing', menu))
             
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', '', jm.show_and_focus),
            ActionSpec('Rings and Torus', 'Control Rings and Torus', '', rd.show_and_focus)
         ]
        ))
