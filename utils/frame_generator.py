from datetime import datetime
import json
from ui.common import get_settings, get_runtime, get_catalog_handler

class SpacecraftFrameGenerator:
    name = 'majis_base'
    template = """\\begindata
      TKFRAME_-28400_AXES   = ( 3, 1, 2 )
      TKFRAME_-28400_ANGLES = ( {angles} )
      TKFRAME_-28200_AXES   = ( 3, 1, 2 )
      TKFRAME_-28200_ANGLES = ( {angles} )
\\begintext
"""
    catalog = None

    def frame_content(self, angles):
        # Edit TK frame
        return self.template.format(
        angles=','.join(str(angle) for angle in angles),
    )

    def spice_catalog_content(self, kernel_path):
        return json.dumps({
        "version": "1.0",
        "name": "ESS-Plugin Kernel",
        "spiceKernels": [
            kernel_path
        ]}, indent=2)

    def update(self, angles):
        handler = get_catalog_handler()

        if self.catalog is not None:
            handler.remove_catalog(self.catalog)

        run_time = get_runtime()
        session_path = run_time.get('working_dir')

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        frame_filename = session_path + '/juice_' + self.name + '_' + timestamp + '.tf'

        self.catalog = session_path + '/juice_' + self.name + '_' + timestamp + '.json'

        with open(frame_filename, "wb") as local_file:
            local_file.write(self.frame_content(angles).encode())

        with open(self.catalog, "wb") as local_file:
            local_file.write(self.spice_catalog_content(frame_filename).encode())

        handler.add_catalog(self.catalog)


class MajisFrameGenerator(SpacecraftFrameGenerator):
    name = 'majis_visnir'
    template = """\\begindata
      TKFRAME_-28410_AXES   = ( 1, 2, 3 )
      TKFRAME_-28410_ANGLES = ( {angles} )
\\begintext
"""
