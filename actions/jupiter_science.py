from ui.common import get_runtime, get_catalog_handler
import os
import cosmoscripting


STRUCTURE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scenes', 'data', 'juice')

def trigger_structure(filename, id, action):

    cosmo = cosmoscripting.Cosmo()


    rt = get_runtime()
    handler = get_catalog_handler()

    is_loaded = rt.get('active_' + id, False)
    if not is_loaded:
        handler.add_catalog(os.path.join(STRUCTURE_FOLDER, filename))
        rt.set('active_' + id, True)

    visible = not rt.get('visible_' + id, False)
    rt.set('visible_' + id, visible)

    action.setChecked(visible)
    
    if visible:
        cosmo.showObject(id)
    else:
        cosmo.hideObject(id)
