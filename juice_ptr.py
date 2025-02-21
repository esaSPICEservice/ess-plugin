
import cosmoscripting
import os
import sys
import traceback

cosmo = cosmoscripting.Cosmo()

def my_except_hook(exctype, value, tb):
    print("Generic Handler")
    traceback.print_exc()
    cosmo.quit()
sys.excepthook = my_except_hook



# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from ui.main_ui import get_main_window, create_ui
from ui.simulator_ui import PTREditorDialog

main_window = get_main_window()

create_ui('juice.json')

ptr_editor = PTREditorDialog(main_window)
ptr_editor.show_and_focus()

cosmo.showInfoText()
cosmo.unloadLastCatalog()

