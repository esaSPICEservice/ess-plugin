from datetime import datetime
import json
from ui.common import get_settings, get_runtime, get_catalog_handler

class MajisFrameGenerator:

    def frame_content_old(self, angles):
        template = """\\begindata

      FRAME_JUICE_MAJIS_POINTER = 1234567
      FRAME_1234567_NAME       = 'JUICE_MAJIS_POINTER'
      FRAME_1234567_CLASS      = 4
      FRAME_1234567_CLASS_ID   = 1234567
      FRAME_1234567_CENTER     = -28400
 
      TKFRAME_1234567_SPEC     = 'ANGLES'
      TKFRAME_1234567_RELATIVE = 'JUICE_MAJIS_BASE'
      TKFRAME_1234567_ANGLES   = ( {angles} )
      TKFRAME_1234567_AXES     = (       1,        2,   3 )
      TKFRAME_1234567_UNITS    = 'DEGREES'

\\begintext
"""
        return template.format(
        angles=','.join(str(angle) for angle in angles)
    )

    def frame_content(self, angles):
        template = """\\begindata
      TKFRAME_1234567_ANGLES   = ( {angles} )
\\begintext
"""
        return template.format(
        angles=','.join(str(angle) for angle in angles)
    )

    def spice_catalog_content(self, kernel_path):
        return json.dumps({
        "version": "1.0",
        "name": "ESS-Plugin Kernel",
        "spiceKernels": [
            kernel_path
        ]}, indent=2)

    def update(self, angles):

        run_time = get_runtime()
        session_path = run_time.get('working_dir')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        frame_filename = session_path + '/juice_majis_' + timestamp + '.tf'
        catalog_filename = session_path + '/juice_majis_' + timestamp + '.json'

        with open(frame_filename, "wb") as local_file:
            local_file.write(self.frame_content(angles).encode())

        with open(catalog_filename, "wb") as local_file:
            local_file.write(self.spice_catalog_content(frame_filename).encode())

        handler = get_catalog_handler()
        handler.add_catalog(catalog_filename)
