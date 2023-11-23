
from ui.common import get_main_window, MenuSpec, ActionSpec, add_menu, set_settings_handler
from ui.mk_ui import MkLoaderDialog
from ui.simulator_ui import PTREditorDialog

def create_ui():
    set_settings_handler()

    main_window = get_main_window()

    bd = PTREditorDialog(main_window)
    mk = MkLoaderDialog(main_window)
    add_menu(main_window, MenuSpec('Scenes', 
                                   [
                                       ActionSpec('Metakernel Load', 'Build a basic scene', '', mk.show_and_focus),
                                       ActionSpec('PTR simulation', 'Execute OSVE', '', bd.show_and_focus)
                                    ]))

