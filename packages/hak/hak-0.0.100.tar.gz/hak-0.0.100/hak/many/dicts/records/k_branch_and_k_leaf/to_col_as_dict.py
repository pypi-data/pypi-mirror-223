from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.one.dict.unit.to_str import f as unit_to_str

# get_column
# records_k_branch_k_leaf_to_col_as_dict
f = lambda records, k_branch, k_leaf: {
  'header': k_leaf,
  'unit': unit_to_str(records[0][k_branch][k_leaf]['unit']),
  'values': [r[k_branch][k_leaf] for r in records]
}

def t_prices_apples():
  x = {
    'records': [
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
    ],
    'k_branch': 'prices',
    'k_leaf': 'apples'
  }
  y = {
    'header': 'apples',
    'unit': '$/apple',
    'values': [
      make_rate(1, 4, {'$': 1, 'apple': -1}),
      make_rate(3, 4, {'$': 1, 'apple': -1})
    ]
  }
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_prices_apples(): return pf('!t_prices_apples')
  return True
