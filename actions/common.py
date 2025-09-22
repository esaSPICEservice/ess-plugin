
from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec, show_url_in_browser, ExtendedActionSpec
from ui.mars_ui import MarsDialog
from ui.moons_ui import MoonsDialog
from ui.navigation_ui import NavigationDialog
from ui.observations_ui import ObservationsDialog
from ui.rings_ui import RingsDialog
from .jupiter_science import trigger_structure
from functools import partial
from simulator.osve import __version__

def add_juice_menu():
    main_window = get_main_window()
    jm = MoonsDialog(main_window)
    rd = RingsDialog(main_window)
    add_menu(main_window, MenuSpec(
        'Jupiter structures', 
        [
            ActionSpec('Jovian Moons', 'Control Jovian Moons', '', jm.show_and_focus),
            ActionSpec('Rings and Torus', 'Control Rings and Torus', '', rd.show_and_focus),
            ExtendedActionSpec('Jupiter Aurora', 'Show Jupiter Aurora', '', partial(trigger_structure,'jupiter_main_aurora.json', 'jupiter_main_aurora')),
            ExtendedActionSpec('Jupiter Belt Inner 45 double', '', '', partial(trigger_structure,'jupiter_belts_inner_45deg_double.json', 'Dipole_inner_45deg_double')),
            ExtendedActionSpec('Jupiter Belt Inner 45', '', '', partial(trigger_structure,'jupiter_belts_inner_45deg.json', 'Dipole_inner_45deg')),
            ExtendedActionSpec('Jupiter Belt Inner 90', '', '', partial(trigger_structure,'jupiter_belts_inner_90deg.json', 'Dipole_inner_90deg')),
            ExtendedActionSpec('Jupiter Belt Inner', '', '', partial(trigger_structure,'jupiter_belts_inner.json', 'Dipole_inner')),
            ExtendedActionSpec('Jupiter Belt Middle 45 double', '', '', partial(trigger_structure,'jupiter_belts_middle_45deg_double.json', 'Dipole_middle_45deg_double')),
            ExtendedActionSpec('Jupiter Belt Middle 45', '', '', partial(trigger_structure,'jupiter_belts_middle_45deg.json', 'Dipole_middle_45deg')),
            ExtendedActionSpec('Jupiter Belt Middle 90', '', '', partial(trigger_structure,'jupiter_belts_middle_90deg.json', 'Dipole_middle_90deg')),
            ExtendedActionSpec('Jupiter Belt Middle', '', '', partial(trigger_structure,'jupiter_belts_middle.json', 'Dipole_middle')),
            ExtendedActionSpec('Jupiter Belt Outer 45 double', '', '', partial(trigger_structure,'jupiter_belts_outer_45deg_double.json', 'Dipole_outer_45deg_double')),
            ExtendedActionSpec('Jupiter Belt Outer 45', '', '', partial(trigger_structure,'jupiter_belts_outer_45deg.json', 'Dipole_outer_45deg')),
            ExtendedActionSpec('Jupiter Belt Outer 90', '', '', partial(trigger_structure,'jupiter_belts_outer_90deg.json', 'Dipole_outer_90deg')),
            ExtendedActionSpec('Jupiter Belt Outer', '', '', partial(trigger_structure,'jupiter_belts_outer.json', 'Dipole_outer'))            
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
    
    osve_version = 'OSVE v' + __version__

    add_menu(main_window, MenuSpec('Juice Help',
                                   [
                                       ActionSpec('Science Models', 'Browse Science Models Help', '', show_science_models_help),
                                       ActionSpec('SPICE data for JUICE', 'Browse Science Models Help', '', show_spice_help),
                                       ActionSpec(osve_version, 'OSVE help', '', show_osve_help)
                                   ]
                                   ))

def show_science_models_help():
    show_url_in_browser('https://juicesoc.esac.esa.int/help/scimod')

def show_spice_help():
    show_url_in_browser('https://www.cosmos.esa.int/web/spice/spice-for-juice')

def show_osve_help():
    show_url_in_browser('https://juicesoc.esac.esa.int/help/osve')
    
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

