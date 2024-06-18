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

    def __init__(self, items=None):
        self.version = '1.0'
        self.name = 'ESS-Plugin generated'
        self.items = items if items is not None else []

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



def append_observation(items, index, body, sensor_name, start, end, color):

    # "1997-10-15 09:26:08.390 UTC"

    obs_json =  {
        "class": "observation",
        "name": "OBSERVATION_" + str(index),
        "startTime": start,
        "endTime": end,
        "center": body,
        "trajectoryFrame": {
            "type": "BodyFixed",
            "body": body
        },
        "bodyFrame": {
            "type": "BodyFixed",
            "body": body
        },
        "geometry": {
            "type": "Observations",
            "sensor": sensor_name,
            "groups": [
            {
                "startTime": start,
                "endTime": end,
                "obsRate": 0
            }
            ],
            "footprintColor": color,
            "footprintOpacity": 0.4,
            "showResWithColor": False,
            "sideDivisions": 125,
            "alongTrackDivisions": 500,
            "shadowVolumeScaleFactor": 1.75,
            "fillInObservations": False
        }
    }
    
    items.append(obs_json)