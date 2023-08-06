from hak.one.dict.get_sorted_keys import f as get_sorted_keys
from hak.pxyz import f as pxyz

# records_to_first_record_sorted_keys
f = lambda records: get_sorted_keys(records[0])

def t():
  x = [{'z': 0, 'y': 1, 'x': 2}, {}]
  y = ['x', 'y', 'z']
  z = f(x)
  return pxyz(x, y, z)
