import struct
import json
import os
from typing import Any

class Record:
    def __init__(self, seq) -> None:
        self.id = seq[0]
        self.ra = seq[1]
        self.dec = seq[2]
        self.vmag = seq[3]
        self.bv = seq[4]

    @staticmethod
    def from_json(json_obj):
        seq = []
        seq.append(json_obj.get("id"))
        seq.append(json_obj.get("ra"))
        seq.append(json_obj.get("dec"))
        seq.append(json_obj.get("vmag"))
        seq.append(json_obj.get("bv"))

        return Record(seq)


def _get(record, field):
    return getattr(record, field) if hasattr(record, field) else record.get(field)

def _generate_record(fout, record):
    fout.write(struct.pack('>I', _get(record, "id")))
    fout.write(struct.pack('>f', _get(record, "ra")))
    fout.write(struct.pack('>f', _get(record, "dec")))
    fout.write(struct.pack('>f', _get(record, "vmag")))
    fout.write(struct.pack('>f', _get(record, "bv")))

def write_to_file(filename, list_records):
    with open(filename, 'bw') as fout:
        for record in list_records:
            _generate_record(fout, record)

def _struct_unpack(data):
    seq = struct.Struct('>I4f').unpack_from(data)
    return Record(seq)

def from_file_records(filename):
    with open(filename, 'rb') as f:
        records = []
        while True:
            data = f.read(5 * 4)
            if not data: break
            s = _struct_unpack(data)
            records.append(s)
        return records

def get_star_names():
    with open(os.path.join(os.path.dirname(__file__), 'data', 'starnames.json'), 'r') as src_json_file:
        star_names = json.load(src_json_file)
    return star_names

def get_star_db():
    return from_file_records(os.path.join(os.path.dirname(__file__), 'data', 'tycho2.stars'))