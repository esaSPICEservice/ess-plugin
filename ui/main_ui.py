
from ui.common import get_main_window, MenuSpec, ActionSpec, add_menu, set_settings_handler, get_runtime, show_url_in_browser
from ui.console_ui import ConsoleDialog
from ui.catalogs_ui import CatalogsDialog
from ui.landing import LandingDialog
from ui.mk_ui import MkLoaderDialog
from ui.simulator_ui import PTREditorDialog
from ui import __version__

def create_ui(settings_filename, ptr_as_default=False):

    set_settings_handler()
    rt = get_runtime()
    rt.load(settings_filename)

    main_window = get_main_window()
    actions = []

    mk = MkLoaderDialog(main_window)
    actions.append(ActionSpec('Metakernel Load', 'Build a basic scene', '', mk.show_and_focus))

    use_ptr = rt.get('use_ptr', False)

    if use_ptr:
        bd = PTREditorDialog(main_window)
        actions.append(ActionSpec('PTR simulation', 'Execute OSVE', 'alt+p', bd.show_and_focus))

    add_menu(main_window, MenuSpec('Scenes', actions))

    cm = ConsoleDialog(main_window)
    cat = CatalogsDialog(main_window)
    add_menu(main_window, MenuSpec('Runtime',
            [
            ActionSpec('Console', 'Runtime console', '', cm.show_and_focus),
            ActionSpec('Catalogs', 'Runtime catalogs', '', cat.show_and_focus),
            ActionSpec('ESS plugin v' + __version__, 'Version of the tool', '', show_plugin_repository)
            ]))

    if ptr_as_default:
        bd.show_and_focus()
    else:
        mk.show_and_focus()


def show_plugin_repository():
    show_url_in_browser('https://s2e2.cosmos.esa.int/bitbucket/projects/SPICE/repos/ess-plugin')
