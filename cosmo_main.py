
import cosmoscripting
import os
import sys

cosmo = cosmoscripting.Cosmo()

# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from ui.main_ui import create_ui

create_ui()

#
# Display a welcome message that will stay on the screen for 10 seconds.
#

cosmo.showInfoText()
#
# Load the catalog
#
cosmo.unloadLastCatalog()

