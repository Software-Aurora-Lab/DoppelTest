from modules.map.proto.map_pb2 import Map
from google.protobuf import text_format


def load_hd_map(filename: str):
    if filename.endswith("bin"):
        return load_hd_map_bin(filename)
    elif filename.endswith("txt"):
        return load_hd_map_txt(filename)
    else:
        raise ValueError(f"Unsupported HD map file format: {filename}")

def load_hd_map_bin(filename: str) -> Map:
    map = Map()
    f = open(filename, 'rb')
    map.ParseFromString(f.read())
    f.close()
    return map

def load_hd_map_txt(filename: str) -> Map:
    map = Map()
    with open(filename, 'r') as f:
        text_format.Parse(f.read(), map)
    return map