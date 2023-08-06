# ignore_overlength_lines

from .k_branch_and_k_leaf.to_col_hor_line import f as records_k_branch_k_leaf_to_col_hor_line
from .to_k_branch_k_leaf_pairs import f as records_to_k_branch_k_leaf_pairs
from hak.cell_lines_to_row_line import f as cell_lines_to_row_line
from hak.one.dict.rate.make import f as make_rate
from hak.pxyz import f as pxyz

# records_to_horizontal_line
f = lambda x: cell_lines_to_row_line([
  records_k_branch_k_leaf_to_col_hor_line(x, a, b)
  for (a, b)
  in records_to_k_branch_k_leaf_pairs(x)
])

def t():
  x = [
    {
      'prices': {
        'apples': make_rate(1, 4, {'$': 1, 'apple': -1}),
        'bananas': make_rate(2, 4, {'$': 1, 'banana': -1})
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
        'bananas': make_rate(4, 4, {'$': 1, 'banana': -1})
      },
      'volumes': {
        'applezzz': make_rate(4, 1, {'apple': 1}),
        'bananazzz': make_rate(5, 1, {'banana': 1}),
        'pearzzzzzz': make_rate(6, 1, {'pear': 1})
      },
      'zloops': {'zloop': make_rate(7, 1, {'zloop': 1})}
    }
  ]
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(x)
  return pxyz(x, y, z)
