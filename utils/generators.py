import json
from dataclasses import dataclass

class Generator:

    def content(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def save(self, local_filename):
        with open(local_filename, "wb") as local_file:
            local_file.write(self.content().encode())


@dataclass
class Sensor:
    """Class for describing a sensor."""
    instr_name: str
    target: str
    frustum_color: str
    sensor_position: str

class SensorGenerator(Generator):
    '''Sensor representation'''

    def __init__(self, sensor, spacecraft):
        self.version = '1.0'
        self.name = 'ESS-Plugin generated'

        name = sensor.instr_name + '_' + sensor.target.upper()
        body = spacecraft

        self.items = [{
            'class': 'sensor',
            'name': name,
            'parent': body,
            'center': body,
            'trajectoryFrame': {
                'type': 'BodyFixed',
                'body': body
            },

            'geometry': {
                'type': 'Spice',
                'instrName':  sensor.instr_name,
                'target':  sensor.target,
                'range': 12000,
                'rangeTracking': True,
                'frustumColor':  sensor.frustum_color,
                'frustumOpacity': 0.3,
                'gridOpacity': 0.3,
                'footprintOpacity': 0.5,
                'sideDivisions': 125,
                'onlyVisibleDuringObs': False
            }

        }]

        if sensor.sensor_position:
            self.items[0]['trajectory'] = {
                "type": "FixedPoint",
                "position": sensor.sensor_position
            }