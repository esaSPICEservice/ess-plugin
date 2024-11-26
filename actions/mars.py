import json
import os
import cosmoscripting


TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scenes', 'data', 'm-matisse')

def get_structures():

    structures = {}
    # structure_files = [
    #     "mars_bowshock.json",
    #     "mars_magnetic_boundary.json"
    #     ]

    # for filename in structure_files:
    #     structure_path = os.path.join(TEMPLATE_FOLDER, filename)
    #     with open(structure_path, 'r') as structure_file:
    #         moon_info = json.load(structure_file)
    #         group_name = moon_info.get('name')
    #         structures[group_name] = [moon.get('name') for moon in moon_info.get('items')]
    structures['Magnetic Field'] = [
        "Mars_Bowshock",
        "Mars_Magnetic_Boundary"
    ]
    return structures


def toggle_structure(value, name):
    cosmo = cosmoscripting.Cosmo()

    if value:
        cosmo.showObject(name)
        cosmo.showTrajectory(name)
    else:
        cosmo.hideObject(name)
        cosmo.hideTrajectory(name)
