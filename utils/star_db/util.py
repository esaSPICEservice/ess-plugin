import json
from utils.star_db.tycho2 import write_to_file, get_star_db, get_star_names, Record

def find_in_list(list_of_items: list, field_name: str, id: int):
    found = list(filter(lambda item: item.get(field_name) == id, list_of_items))
    if len(found) > 0:
        return found[0]
    return None 

def update_stars(candidates, dst_db, dst_json):

    # We read the original start_names
    star_names = get_star_names()

    # We read the DB
    records = get_star_db()

    # Ids of the candidates
    candidates_ids = list(map(lambda candidate:  candidate.get("id"), candidates))
    stars = []

    for record in records:
        star_id = record.id
        if star_id in candidates_ids:
            candidates_ids.remove(star_id)
            candidate = find_in_list(candidates, 'id', star_id)
            name = candidate.get('name')
            star_in_json = find_in_list(star_names, 'tychoId', star_id)
            if star_in_json != None:
                star_in_json["name"] = name
            else:
                star_names.append({'tychoId': star_id , 'name': name})
            record.vmag = 1.044
        stars.append(record)

 
    for star_id in candidates_ids:
        candidate = find_in_list(candidates, 'id', star_id)
        name = candidate.get('name')
        candidate['vmag'] = 1.044
        candidate['bv'] = 0.9
        stars.append(Record.from_json(candidate))
        star_names.append({'tychoId': candidate.get("id") , 'name': name})
 
    write_to_file(dst_db, stars)

    # finally we dump the updated starts

    with open(dst_json, 'w') as dst_json_file:
        json.dump(star_names, dst_json_file, indent=2)

    print('Files updated')