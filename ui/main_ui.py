
from ui.common import get_main_window, MenuSpec, ActionSpec, add_menu
from ui.mk_ui import MkLoaderDialog
from ui.simulator_ui import PTREditorDialog


def create_ui():
    main_window = get_main_window()
    main_window.setWindowOpacity(0.9)

    bd = PTREditorDialog(main_window)
    mk = MkLoaderDialog(main_window)
    add_menu(main_window, MenuSpec('Scenes', 
                                   [
                                       ActionSpec('Metakernel Load', 'Execute OSVE', 'Alt+P', mk.show_and_focus),
                                       ActionSpec('PTR simulation', 'Execute OSVE', 'Alt+P', bd.show_and_focus)
                                    ]))

