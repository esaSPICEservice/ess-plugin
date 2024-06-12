import json

SENSOR_SUFFIX =  '_SENSOR'
class Generator:

    def content(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def save(self, local_filename):
        with open(local_filename, "wb") as local_file:
            local_file.write(self.content().encode())


class Sensor:
    """Class for describing a sensor."""
    def __init__(self, instr_name, target, frustum_color, sensor_position):
        self.instr_name = instr_name
        self.target = target
        self.frustum_color = frustum_color
        self.sensor_position = sensor_position

class SensorGenerator(Generator):
    '''Sensor representation'''

    def __init__(self):
        self.version = '1.0'
        self.name = 'ESS-Plugin generated'
        self.items = []

    def append(self, sensor, spacecraft):
        name = sensor.instr_name + SENSOR_SUFFIX
        body = spacecraft

        sensor_json = {
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
                'frustumOpacity': 0.0,
                'gridOpacity': 0.3,
                'footprintOpacity': 0.5,
                'sideDivisions': 125,
                'onlyVisibleDuringObs': False
            }

        }
        
        if sensor.sensor_position:
            sensor_json['trajectory'] = {
                "type": "FixedPoint",
                "position": sensor.sensor_position
        }

        self.items.append(sensor_json)
