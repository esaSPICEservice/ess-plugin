import cosmoscripting
from simulator.wrapper import simulate
from utils.block_parser import BlockParser

from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog

def execute_ptr(mk, content):
    start_time = validate_ptr(content)
    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    catalog = simulate(mk, content)
    cosmo.loadCatalogFile(catalog)
    after_load()
    cosmo.setTime(start_time + ' UTC')
    cosmo.gotoObject('JUICE', 0)

def validate_ptr(content):
    parser = BlockParser(content)
    parser.process()
    return parser.start_times[0]

def after_load():
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', 'Alt+J', jm.show_and_focus),
            ActionSpec('Jupiter Rings', 'Control Jovian Moons', 'Alt+J', rd.show_and_focus)
         ]
        ))