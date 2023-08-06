# ignore_overlength_lines

from .to_leaf_col_width import f as records_k_branch_k_leaf_to_leaf_col_width
from .to_unpadded_unit_str import f as records_k_branch_k_leaf_to_unpadded_unit_str
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# f_w
# records_k_branch_k_leaf_to_unit_cell_str
def f(records, k_branch, k_leaf):
  _0 = records_k_branch_k_leaf_to_unpadded_unit_str(records, k_branch, k_leaf)
  _1 = records_k_branch_k_leaf_to_leaf_col_width(records, k_branch, k_leaf)
  return f"{_0:>{_1}}"

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

def t_prices_apples():
  x = {'records': _records, 'k_branch': 'prices', 'k_leaf': 'apples'}
  y = '$/apple'
  z = f(**x)
  return pxyz(x, y, z)

def t_prices_bananas():
  x = {'records': _records, 'k_branch': 'prices', 'k_leaf': 'bananas'}
  y = '$/banana'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_applezzz():
  x = {'records': _records, 'k_branch': 'volumes', 'k_leaf': 'applezzz'}
  y = '   apple'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_bananazzz():
  x = {'records': _records, 'k_branch': 'volumes', 'k_leaf': 'bananazzz'}
  y = '   banana'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_pearzzzzzz():
  x = {'records': _records, 'k_branch': 'volumes', 'k_leaf': 'pearzzzzzz'}
  y = '      pear'
  z = f(**x)
  return pxyz(x, y, z)

def t_zloops_zloop():
  x = {'records': _records, 'k_branch': 'zloops', 'k_leaf': 'zloop'}
  y = ' zloop'
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_prices_apples(): return pf('!t_prices_apples')
  if not t_prices_bananas(): return pf('!t_prices_bananas')
  if not t_volumes_applezzz(): return pf('!t_volumes_applezzz')
  if not t_volumes_bananazzz(): return pf('!t_volumes_bananazzz')
  if not t_volumes_pearzzzzzz(): return pf('!t_volumes_pearzzzzzz')
  if not t_zloops_zloop(): return pf('!t_zloops_zloop')
  return True
