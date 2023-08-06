# ignore_overlength_lines
from ..k_branch_k_leaf_and_record_index.to_cell_str import f as records_k_branch_k_leaf_record_index_to_cell_str
from ..to_k_branch_k_leaf_pairs import f as recs_to_k_b_k_l_pairs
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# f_y
# records_and_record_index_to_padded_cell_values_of_col_width
f = lambda records, record_index: [
  records_k_branch_k_leaf_record_index_to_cell_str(
    records,
    k_branch,
    k_leaf,
    record_index
  )
  for (k_branch, k_leaf)
  in recs_to_k_b_k_l_pairs(records)
]

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

def t_0():
  x = {'records': _records, 'record_index': 0}
  y = ['   0.25', '    0.50', '    1.00', '     2.00', '      3.00', '  7.00']
  z = f(**x)
  return pxyz(x, y, z)

def t_1():
  x = {'records': _records, 'record_index': 1}
  y = ['   0.75', '    1.00', '    4.00', '     5.00', '      6.00', '  7.00']
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  return True
