from actions.common import add_hera_menu, add_juice_menu, add_tgo_menu, add_mmatisse_menu
import cosmoscripting
from scenes.generator import create_cosmo_scene, generate_working_dir
from actions.time_navigation import goto_date
from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec, get_runtime, remove_menu  
from ui.moons_ui import MoonsDialog
from ui.rings_ui import RingsDialog

def execute(mk, extra_kernels, date):

    working_dir = generate_working_dir()

    catalog, sensor_catalog = create_cosmo_scene(working_dir, mk, extra_kernels)

    cosmo = cosmoscripting.Cosmo()
    cosmo.unloadLastCatalog()
    cosmo.loadCatalogFile(catalog)
    cosmo.loadCatalogFile(sensor_catalog)
    after_load()
    goto_date(date)



def after_load():
    main_window = get_main_window()
    runtime = get_runtime()
    mission = runtime.get('mission')

    if mission is None:
        return
    elif mission.lower() == 'tgo':
        add_tgo_menu()
    elif mission.lower() == 'hera':
        add_hera_menu()
    elif mission.lower() == 'm-matisse':
        add_mmatisse_menu()
    elif mission.lower() == 'juice' or mission.lower() == 'juice_ptr':
        add_juice_menu()
        remove_menu(main_window, 'Pointing')