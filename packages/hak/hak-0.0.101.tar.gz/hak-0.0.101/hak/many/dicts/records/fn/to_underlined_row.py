# ignore_overlength_lines

from ..k_branch_and_k_leaf.to_leaf_cell import f as records_k_branch_k_leaf_to_leaf_cell
from ..k_branch_and_k_leaf.to_unit_cell_str import f as records_k_branch_k_leaf_to_unit_cell_str
from ..to_horizontal_line import f as records_to_horizontal_line
from ..to_row_using_fn import f as records_to_row_using_fn
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# records_and_fn_to_underlined_row
f = lambda records, fn: [
  records_to_row_using_fn(records, fn),
  records_to_horizontal_line(records)
]

from hak.one.dict.rate.make import f as make_rate
_records = [
  {
    'prices': {
      'apples': make_rate(1, 4, {'$': 1, 'apple': -1}),
      'bananas': make_rate(1, 2, {'$': 1, 'banana': -1})
    },
    'volumes': {
      'applezzz': make_rate(1, 1, {'apple': 1}),
      'bananazzz': make_rate(2, 1, {'banana': 1}),
      'pearzzzzzz': make_rate(3, 1, {'pear': 1})
    },
    'zloops': {'zloop': make_rate(7, 1, {'zloop': 1})}
  }, 
  {
    'prices': {
      'apples': make_rate(3, 4, {'$': 1, 'apple': -1}),
      'bananas': make_rate(1, 1, {'$': 1, 'banana': -1})
    },
    'volumes': {
      'applezzz': make_rate(4, 1, {'apple': 1}),
      'bananazzz': make_rate(5, 1, {'banana': 1}),
      'pearzzzzzz': make_rate(6, 1, {'pear': 1})
    },
    'zloops': {'zloop': make_rate(7, 1, {'zloop': 1})}
  }
]

def t_leaf_keys():
  x = _records
  y = [
    '|  apples |  bananas | applezzz | bananazzz | pearzzzzzz |  zloop |',
    '|---------|----------|----------|-----------|------------|--------|'
  ]
  z = f(x, records_k_branch_k_leaf_to_leaf_cell)
  return pxyz(x, y, z)

def t_units():
  x = _records
  y = [
    '| $/apple | $/banana |    apple |    banana |       pear |  zloop |',
    '|---------|----------|----------|-----------|------------|--------|'
  ]
  z = f(x, records_k_branch_k_leaf_to_unit_cell_str)
  return pxyz(x, y, z)

def t():
  if not t_leaf_keys(): return pf('!t_leaf_keys')
  if not t_units(): return pf('!t_units')
  return True
