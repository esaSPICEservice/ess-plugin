from datetime import datetime
import json
import math
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
        frame_filename = session_path + '/' + self.name + '_' + timestamp + '.tf'

        self.catalog = session_path + '/' + self.name + '_' + timestamp + '.json'

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


class SwiFrameGenerator(SpacecraftFrameGenerator):
    name = 'swi'
    template = """\\begindata
      TKFRAME_1234567_AXES   = ( 1, 2, 3 )
      TKFRAME_1234567_ANGLES = ( {angles} )
\\begintext
"""


class PhebusFrameGenerator(SpacecraftFrameGenerator):
    name = 'phebus'
    template = """\\begindata
      TKFRAME_1234567_AXES   = ( 3, 2, 1 )
      TKFRAME_1234567_ANGLES = ( {angles} )
\\begintext
"""

    def phebus_to_euler(self, s):

        d = math.radians(100.0)
        s = math.radians(s)

        z_fov = [
            math.sin(d) * math.cos(s - math.pi / 4.0),
            math.cos(d),
            -math.sin(d) * math.sin(s - math.pi / 4.0)
        ]

        y_fov = [
            math.sin(d/2.0)**2 * math.cos(2.0 * s),
            -math.sin(d) * math.sin(s - math.pi / 4.0),
            -math.sin(d/2.0)**2 * math.sin(2.0 * s)
            - math.cos(d/2.0)**2
        ]

        # cross product y × z
        x_fov = [
            y_fov[1]*z_fov[2] - y_fov[2]*z_fov[1],
            y_fov[2]*z_fov[0] - y_fov[0]*z_fov[2],
            y_fov[0]*z_fov[1] - y_fov[1]*z_fov[0]
        ]

        R = [x_fov, y_fov, z_fov]
        euler = self.rotationMatrixToEulerAngles(R)

        # We need to invert the angles

        return [-1 * euler[0], -1 * euler[1], -1 * euler[2]]



    def rotationMatrixToEulerAngles(self,R):

        sy = math.sqrt(R[2][2]**2 + R[1][2]**2)
        singular = sy < 1e-6

        if not singular:
            x = math.degrees(math.atan2(R[0][1], R[0][0]))
            y = math.degrees(math.atan2(-R[0][2], sy))
            z = math.degrees(math.atan2(R[1][2], R[2][2]))
        else:
            x = math.degrees(math.atan2(-R[1][0], R[1][1]))
            y = math.degrees(math.atan2(-R[0][2], sy))
            z = 0.0

        return [x, y, z]
