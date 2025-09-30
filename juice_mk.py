
import cosmoscripting
import os
import sys
import traceback

cosmo = cosmoscripting.Cosmo()

def my_except_hook(exctype, value, tb):
    print("[EXCEPTION HANDLER] " + value)
    traceback.print_exc()
    cosmo.quit()
sys.excepthook = my_except_hook



# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from ui.main_ui import get_main_window, create_ui
from ui.common import get_catalog_handler

main_window = get_main_window()

create_ui('juice.json', False)

cosmo.showInfoText()
ch = get_catalog_handler()
ch.clean_catalogs()

