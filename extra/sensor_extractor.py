import spiceypy as sp
import re
from spiceypy.utils.exceptions import NotFoundError
import json
import argparse


def get_str(var_name):
    try:
        name = sp.gcpool(var_name, 0, 1)
        return name[0]
    except NotFoundError:
        return get_body_name(int(extract_id(var_name)))

def get_body_name(id):
    try:
        name = sp.bodc2s(id)
        return name
    except NotFoundError:
        return f' {id} not found'


def get_float(var_name):
    try:
        value = sp.gdpool(var_name, 0, 1)
        return value[0]
    except NotFoundError:
        return None


def get_fov_size(id):
    ref_angle = get_float(f'INS{id}_FOV_REF_ANGLE')
    cross_angle = get_float(f'INS{id}_FOV_CROSS_ANGLE')
    unit = get_str(f'INS{id}_FOV_ANGLE_UNITS')
    if ref_angle and cross_angle:
        return 2 * max(ref_angle, cross_angle) * sp.convrt(1, unit, 'DEGREES')
    elif ref_angle:
        return 2 * ref_angle * sp.convrt(1, unit, 'DEGREES')
    elif cross_angle:
        return 2 * ref_angle * sp.convrt(1, unit, 'DEGREES')
    else:
        return 0


def get_definition(id):
    return {
        'name': get_str(f'INS{id}_FOV_NAME'),
        'fov_frame': get_str(f'INS{id}_FOV_FRAME'),
        'size': get_fov_size(id),
        'color': [0, 0.6, 0]
    }


def extract_id(name):
    parts = re.split('_|-', name)
    return '-' + parts[1]

def get_all_instruments_ids():
    max_number = 1000
    names = sp.gnpool('INS-*_FOV_FRAME', 0, max_number)
    return list(map(extract_id, names))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='The script generates a JSON description of the field of views defined in a metakernel')
    parser.add_argument('-m', help='Path to the metakernel', required=True)

    args = parser.parse_args()
    sp.furnsh(args.m)
    instrument_ids = get_all_instruments_ids()
    definitions = sorted(list(map(get_definition, instrument_ids)), key=lambda x: x.get('name'))

    sensors = {}
    sensors_counter = {}
    boresights = []
    LIMIT = 56

    for definition in definitions:
        if 'PEP' in definition.get('name'):
            name = definition.get('name')
            size = definition.get('size')
            fov_name = definition.get('fov_frame')
            parts = name.split('_')
            if len(parts) >= 2:
                sc = parts[0]
                definition['spacecraft'] = sc
                del definition['size']
                
                key = '_'.join(fov_name.split('_')[0:3])
                counter_key = key
                if counter_key not in sensors_counter:
                    sensors_counter[counter_key] = 0
                sensors_counter[counter_key] += 1
                counter = sensors_counter[counter_key]

                if counter > LIMIT:
                    key = f'{key}{counter // LIMIT:02d}'
                    
                    
                key = key.replace('JUICE_PEP_', 'P').upper()
                
                if key not in sensors:
                    sensors[key] = []
                sensors[key].append(definition)
                
            boresights.append({
                "name": name,
                "fov_frame": fov_name,
                "size": size
            })

    cnf = { "sensors": sensors}
    with open('sensor_section.json', 'w') as sensor_file:
        json.dump(cnf, sensor_file, indent=2)
    