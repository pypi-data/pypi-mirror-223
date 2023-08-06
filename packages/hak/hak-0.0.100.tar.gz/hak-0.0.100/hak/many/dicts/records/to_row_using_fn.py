# ignore_overlength_lines

from .k_branch_and_k_leaf.to_leaf_cell import f as records_k_branch_k_leaf_to_leaf_cell
from .k_branch_and_k_leaf.to_unit_cell_str import f as records_k_branch_k_leaf_to_unit_cell_str
from .to_k_branch_k_leaf_pairs import f as records_to_k_b_k_l_pairs
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.row_as_cells_to_row_as_str import f as row_as_cells_to_row_as_str

# f_t
# records_to_row_using_fn
f = lambda records, fn: row_as_cells_to_row_as_str([
  fn(records, k_branch, k_leaf)
  for (k_branch, k_leaf)
  in records_to_k_b_k_l_pairs(records)
])

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

def t_a():
  x = {
    'records': _records,
    'fn': records_k_branch_k_leaf_to_leaf_cell
  }
  y  = '|  apples |  bananas | applezzz | bananazzz | pearzzzzzz |  zloop |'
  z = f(**x)
  return pxyz(x, y, z)

def t_b():
  x = {
    'records': _records,
    'fn': records_k_branch_k_leaf_to_unit_cell_str
  }
  y  = '| $/apple | $/banana |    apple |    banana |       pear |  zloop |'
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
