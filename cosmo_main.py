
import cosmoscripting
import os
import sys

cosmo = cosmoscripting.Cosmo()

# prepare and load the libraries
sys.path.append(os.path.abspath(cosmo.scriptDir()))
from utils.filesystem import get_output_folder
from ui.osve_ui import create_ui
from ptwrapper.wrapper import test

mk = '/Users/randres/juice_repo/juice_crema_5_1_150lb_23_1_v435_20230918_001.tm'
content = """
<prm>
  <body>
    <segment>
      <data>
        <timeline frame="SC">
                <block ref="OBS">
                    <startTime>2032-05-15T20:00:00</startTime>
                    <endTime>2032-05-15T20:15:00</endTime>
                    <attitude ref="terminator">
                        <boresight ref="SC_Zaxis" />
                        <surface ref="Jupiter" />
                        <phaseAngle ref="powerOptimised">
                            <yDir> false </yDir>
                        </phaseAngle>
                    </attitude>
                </block>
        </timeline>
      </data>
    </segment>
  </body>
</prm>
"""



create_ui()

#
# Display a welcome message that will stay on the screen for 10 seconds.
#
cosmo.hideSurfaceFeatureLabels()
#cosmo.hideSpiceMessages()
cosmo.showInfoText()
cosmo.setWindowResolution('xga')
#
# Load the catalog
#
cosmo.unloadLastCatalog()

catalog = test(mk, content)
cosmo.loadCatalogFile(catalog)

cosmo.setTime('2032-05-15T20:00:00Z')
cosmo.gotoObject('JUICE')