import cosmoscripting
from scenes.generator import create_cosmo_scene, generate_working_dir
from actions.time_navigation import goto_date
from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog

def execute(mk, extra_kernels, date):

    working_dir = generate_working_dir()

    catalog = create_cosmo_scene(working_dir, mk, extra_kernels)

    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    cosmo.loadCatalogFile(catalog)
    after_load()
    goto_date(date)



def after_load():
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', '', jm.show_and_focus),
            ActionSpec('Rings and Torus', 'Control Rings and Torus', '', rd.show_and_focus)
         ]
        ))