from ui.common import get_runtime, get_catalog_handler
import os
import cosmoscripting


STRUCTURE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scenes', 'data', 'juice')
AURORA_OBJECT_NAME = 'jupiter_main_aurora'

def trigger_aurora():
    cosmo = cosmoscripting.Cosmo()

    rt = get_runtime()
    handler = get_catalog_handler()


    is_loaded = rt.get('active_aurora', False)
    if not is_loaded:
        handler.add_catalog(os.path.join(STRUCTURE_FOLDER, 'jupiter_main_aurora.json'))
        rt.set('active_aurora', True)

    visible = not rt.get('visible_aurora', False)
    rt.set('visible_aurora', visible)

    if visible:
        cosmo.showObject(AURORA_OBJECT_NAME)
    else:
        cosmo.hideObject(AURORA_OBJECT_NAME)
