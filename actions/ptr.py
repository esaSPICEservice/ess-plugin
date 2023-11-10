import os
import cosmoscripting
from simulator.wrapper import simulate
from ui.blocks_ui import BlocksDialog
from utils.block_parser import BlockParser

from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog

def execute_ptr(mk, content):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    catalog, root_scenario = simulate(mk, content)
    cosmo.loadCatalogFile(catalog)
    after_load(root_scenario)
    cosmo.setTime(start_time + ' UTC')
    cosmo.gotoObject('JUICE', 0)
    cosmo.setCameraToBodyFixedFrame()
    cosmo.setCameraPosition([0.0, 0.0, -0.07]).wait(1)
    cosmo.setCameraOrientation([0.0, 0.0, 1.0]).wait(1)

def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]

def after_load(root_scenario):
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)

    resolved_ptr = os.path.join(root_scenario, 'output', 'ptr_resolved.ptx')

    bp = BlocksDialog(main_window, resolved_ptr)
    add_menu(main_window, MenuSpec(
        'Pointing', 
        [
            ActionSpec('Blocks', 'Show pointing blocks', '', bp.show_and_focus),
         ]
        ))
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', '', jm.show_and_focus),
            ActionSpec('Rings and Torus', 'Control Rings and Torus', '', rd.show_and_focus)
         ]
        ))
