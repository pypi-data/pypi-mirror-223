# ignore_overlength_lines
from .to_first_record_sorted_keys import f as get_K
from .k_branch.to_sorted_leaf_keys import f as records_k_branch_to_sorted_leaf_keys
from hak.pxyz import f as pxyz
from hak.one.dict.rate.make import f as make_rate

# f_n
# records_to_k_branch_k_leaf_pairs
f = lambda x: [
  (a, b)
  for a in get_K(x)
  for b in records_k_branch_to_sorted_leaf_keys(x, a)
]

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
    ('prices',  'apples'    ),
    ('prices',  'bananas'   ),
    ('volumes', 'applezzz'  ),
    ('volumes', 'bananazzz' ),
    ('volumes', 'pearzzzzzz'),
    ('zloops',  'zloop'     )
  ]
  z = f(x)
  return pxyz(x, y, z)
