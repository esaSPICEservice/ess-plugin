
from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec, show_url_in_browser
from ui.mars_ui import MarsDialog
from ui.moons_ui import MoonsDialog
from ui.navigation_ui import NavigationDialog
from ui.observations_ui import ObservationsDialog
from ui.rings_ui import RingsDialog
from .jupiter_science import trigger_aurora



def add_juice_menu():
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', '', jm.show_and_focus),
            ActionSpec('Rings and Torus', 'Control Rings and Torus', '', rd.show_and_focus),
            ActionSpec('Jupiter Aurora', 'Show Jupiter Aurora', '', trigger_aurora),
         ]
        ))

    nv = NavigationDialog(main_window)
    add_menu(main_window, MenuSpec('Navigation', 
                                   [
                                       ActionSpec('Sensors', 'Sensors', '', nv.show_and_focus)
                                    ]))
    nv = NavigationDialog(main_window)
    obs = ObservationsDialog(main_window)
    add_menu(main_window, MenuSpec('Navigation', 
                                   [
                                       ActionSpec('Sensors', 'Sensors', '', nv.show_and_focus),
                                       ActionSpec('Observations', 'Observations', '', obs.show_and_focus)
                                    ]))
    add_menu(main_window, MenuSpec('Juice Help',
                                   [
                                       ActionSpec('Science Models', 'Browse Science Models Help', '', show_science_models_help),
                                       ActionSpec('SPICE data for JUICE', 'Browse Science Models Help', '', show_spice_help)
                                   ]
                                   ))

def show_science_models_help():
    show_url_in_browser('https://juicesoc.esac.esa.int/help/scimod')

def show_spice_help():
    show_url_in_browser('https://www.cosmos.esa.int/web/spice/spice-for-juice')
    
def add_tgo_menu():
    main_window = get_main_window()
    nv = NavigationDialog(main_window)
    obs = ObservationsDialog(main_window)
    add_menu(main_window, MenuSpec('Navigation', 
                                   [
                                       ActionSpec('Sensors', 'Sensors', '', nv.show_and_focus),
                                       ActionSpec('Observations', 'Observations', '', obs.show_and_focus)
                                    ]))

def add_hera_menu():
    main_window = get_main_window()
    nv = NavigationDialog(main_window)
    obs = ObservationsDialog(main_window)
    add_menu(main_window, MenuSpec('Navigation', 
                                   [
                                       ActionSpec('Sensors', 'Sensors', '', nv.show_and_focus),
                                       ActionSpec('Observations', 'Observations', '', obs.show_and_focus)
                                    ]))

def add_mmatisse_menu():
    main_window = get_main_window()
    ms = MarsDialog(main_window)
    add_menu(main_window, MenuSpec(
        'Mars', 
        [
            ActionSpec('Mars Structures', 'Control Mars Structure', '', ms.show_and_focus),
         ]
        ))

    nv = NavigationDialog(main_window)
    obs = ObservationsDialog(main_window)
    add_menu(main_window, MenuSpec('Navigation', 
                                   [
                                       ActionSpec('Sensors', 'Sensors', '', nv.show_and_focus),
                                       ActionSpec('Observations', 'Observations', '', obs.show_and_focus)
                                    ]))

