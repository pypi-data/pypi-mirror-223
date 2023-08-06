# ignore_overlength_lines
from .fn.to_underlined_row import f as records_and_fn_to_underlined_row
from .k_branch_and_k_leaf.to_unit_cell_str import f as records_k_branch_k_leaf_to_unit_cell_str
from hak.one.dict.rate.make import f as make_rate
from hak.pxyz import f as pxyz

# f_units
# records_to_units_row_with_underline
f = lambda x: records_and_fn_to_underlined_row(
  x,
  records_k_branch_k_leaf_to_unit_cell_str
)

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
  y = [
    '| $/apple | $/banana |    apple |    banana |       pear |  zloop |',
    '|---------|----------|----------|-----------|------------|--------|'
  ]
  z = f(x)
  return pxyz(x, y, z)
