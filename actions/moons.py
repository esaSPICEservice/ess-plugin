import json
import os
import cosmoscripting


TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'scenes', 'data', 'juice')

def get_moons():

    moons = {}
    moon_files = [
        'jupiter_minor_moons_ananke_group.json', 
        'jupiter_minor_moons_carme_group.json', 
        'jupiter_minor_moons_inner_group.json',
        'jupiter_minor_moons_pasiphae_group.json',
        'jupiter_minor_moons_prograde_groups.json'
        ]

    for filename in moon_files:
        moons_path = os.path.join(TEMPLATE_FOLDER, filename)
        with open(moons_path, 'r') as moon_file:
            moon_info = json.load(moon_file)
            group_name = moon_info.get('name')
            moons[group_name] = [moon.get('name') for moon in moon_info.get('items')]

    return moons


def toggle_moon(value, name):
    cosmo = cosmoscripting.Cosmo()

    if value:
        cosmo.showObject(name)
        cosmo.showTrajectory(name)
    else:
        cosmo.hideObject(name)
        cosmo.hideTrajectory(name)
