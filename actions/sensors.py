import cosmoscripting
from utils.generators import SENSOR_SUFFIX

sensors = {
    "GAL": ["JUICE_GALA_RXT"],
    "JAN": ["JUICE_JANUS"],
    "JMC": ["JUICE_JMC-1", "JUICE_JMC-2"],
    "MAJ": [
        "JUICE_MAJIS_ENVELOPE",
        "JUICE_MAJIS_VISNIR",
        "JUICE_MAJIS_VISNIR_B2",
        "JUICE_MAJIS_VISNIR_B4",
        "JUICE_MAJIS_IR",
        "JUICE_MAJIS_IR_B2",
        "JUICE_MAJIS_IR_B4",
    ],
    "NAV": ["JUICE_NAVCAM-1", "JUICE_NAVCAM-2"],
    "PJDC": [
        "JUICE_PEP_JDC_PIXEL_000",
        "JUICE_PEP_JDC_PIXEL_080",
        "JUICE_PEP_JDC_PIXEL_176",
        "JUICE_PEP_JDC_PIXEL_004",
        "JUICE_PEP_JDC_PIXEL_084",
        "JUICE_PEP_JDC_PIXEL_180",
        "JUICE_PEP_JDC_PIXEL_008",
        "JUICE_PEP_JDC_PIXEL_088",
        "JUICE_PEP_JDC_PIXEL_184",
        "JUICE_PEP_JDC_PIXEL_012",
        "JUICE_PEP_JDC_PIXEL_092",
        "JUICE_PEP_JDC_PIXEL_188",
    ],
    "STR": ["JUICE_STR-OH1", "JUICE_STR-OH2", "JUICE_STR-OH3"],
    "UVS": ["JUICE_UVS_AP_HP", "JUICE_UVS_SP"],
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
