import cosmoscripting
from utils.generators import SENSOR_SUFFIX

sensors = {
    "JAN": ["JUICE_JANUS"],
    "GAL": ["JUICE_GALA_RXT"],
    "MAJ": ["JUICE_MAJIS_IR"],
    "PEP": ["JUICE_PEP_JDC"],
    "UVS": ["JUICE_UVS_AP_HP", "JUICE_UVS_SP"],
    "STR": ["JUICE_STR-OH1", "JUICE_STR-OH2", "JUICE_STR-OH3"],
}

def get_sensor_list():
    sensor_list = []
    for instrument in sensors:
        sensor_list.extend(sensors[instrument])
    return sensor_list

def get_sensors():
    return sensors


def toggle_sensor(visible, name):
    cosmo = cosmoscripting.Cosmo()
    sensor_id = name + SENSOR_SUFFIX
    if visible:
        cosmo.showObject(sensor_id)
    else:
        cosmo.hideObject(sensor_id)
