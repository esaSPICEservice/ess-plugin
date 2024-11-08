
from ui.common import get_main_window, ActionSpec, add_menu, MenuSpec
from ui.moons_ui import MoonsDialog
from ui.navigation_ui import NavigationDialog
from ui.observations_ui import ObservationsDialog
from ui.rings_ui import RingsDialog



def add_juice_menu():
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