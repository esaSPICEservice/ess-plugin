
import cosmoscripting
import os
import sys
from PyQt5.QtWidgets import QMessageBox

cosmo = cosmoscripting.Cosmo()

def my_except_hook(exctype, value, traceback):
    print("Generic Handler")
    print(exctype, value, traceback)
    cosmo.quit()
sys.excepthook = my_except_hook




# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from ui.main_ui import get_main_window
from ui.stardb_ui import StarDBDialog
from ui.common import get_settings
from utils.star_db.util import update_stars

settings = get_settings()

def create_stars(candidates):
    settings.set('stardb', 'star_list', candidates)
    settings.save()
    dst_json = os.path.join(os.path.abspath('.'), 'starnames.json')
    dst_db = os.path.join(os.path.abspath('.'), 'tycho2.stars')

    if os.path.exists(dst_json) and os.path.exists(dst_db):
        update_stars(candidates, dst_db, dst_json)
        QMessageBox.information(None, "Info", 
                ("The star database has been updated\n"
                 "Cosmographia has to be restarted\n"
                 "for the changes to take effect."))
    else:
        QMessageBox.warning(None, "Info", 
                ("The star database does not exist\n"
                 "Check with the SPICE service\n"
                 "to get assistance.\n",
                 "spice@cosmos.esa.int"))
    # QMessageBox.information(None, "Info", 
    #             ("The star database has been updated\n"
    #              "Cosmographia has to be restarted\n"
    #              "for the changes to take effect."))
    cosmo.quit()

star_list = settings.get('stardb', 'star_list', [])
main_window = get_main_window()
landing = StarDBDialog(main_window)
landing.addFromList(star_list)
landing.show_and_focus(create_stars)

