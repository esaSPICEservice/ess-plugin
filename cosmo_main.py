
import cosmoscripting
import os
import sys

cosmo = cosmoscripting.Cosmo()

# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from utils.filesystem import get_output_folder
from ui.simulator_ui import create_ui

create_ui()

#
# Display a welcome message that will stay on the screen for 10 seconds.
#

cosmo.showInfoText()
cosmo.setWindowResolution('xga')
#
# Load the catalog
#
cosmo.unloadLastCatalog()

