
import cosmoscripting
import os
import sys
import traceback

cosmo = cosmoscripting.Cosmo()

def my_except_hook(exctype, value, tb):
    print("Generic Handler")
    print(exctype, value, tb)
    traceback.print_exc()
    cosmo.quit()
sys.excepthook = my_except_hook



# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from ui.main_ui import get_main_window, create_ui
from ui.landing import LandingDialog

main_window = get_main_window()
landing = LandingDialog(main_window)
landing.show_and_focus(create_ui)

cosmo.showInfoText()
cosmo.unloadLastCatalog()

