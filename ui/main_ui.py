
from ui.common import get_main_window, MenuSpec, ActionSpec, add_menu, set_settings_handler, get_runtime
from ui.landing import LandingDialog
from ui.mk_ui import MkLoaderDialog
from ui.simulator_ui import PTREditorDialog

def create_ui(settings_filename):

    set_settings_handler()
    rt = get_runtime()
    rt.load(settings_filename)

    main_window = get_main_window()
    actions = []
    
    mk = MkLoaderDialog(main_window)
    actions.append(ActionSpec('Metakernel Load', 'Build a basic scene', '', mk.show_and_focus))
    
    sc = rt.get('spacecraft', '')

    if sc == 'JUICE':
        bd = PTREditorDialog(main_window)
        actions.append(ActionSpec('PTR simulation', 'Execute OSVE', '', bd.show_and_focus))

    add_menu(main_window, MenuSpec('Scenes', actions))


