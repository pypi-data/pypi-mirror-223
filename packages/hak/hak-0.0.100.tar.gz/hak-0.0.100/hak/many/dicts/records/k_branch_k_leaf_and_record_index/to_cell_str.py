# ignore_overlength_lines

from ..k_branch_and_k_leaf.to_leaf_col_width import f as get_col_w_fr_k_b_k_l
from hak.one.dict.rate.to_str import f as rate_to_str
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# f_x
# records_k_branch_k_leaf_record_index_to_cell_str
def f(records, k_branch, k_leaf, record_index):
  _0 = get_col_w_fr_k_b_k_l(records, k_branch, k_leaf)
  return f'{rate_to_str(records[record_index][k_branch][k_leaf]):>{_0}}'

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

def t_prices_apples_0():
  x = {
    'records': _records,
    'k_branch': 'prices',
    'k_leaf': 'apples',
    'record_index': 0
  }
  y = '   0.25'
  z = f(**x)
  return pxyz(x, y, z)

def t_prices_bananas_0():
  x = {
    'records': _records,
    'k_branch': 'prices',
    'k_leaf': 'bananas',
    'record_index': 0
  }
  y = '    0.50'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_applezzz_0():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'applezzz',
    'record_index': 0
  }
  y = '    1.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_bananazzz_0():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'bananazzz',
    'record_index': 0
  }
  y = '     2.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_pearzzzzzz_0():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'pearzzzzzz',
    'record_index': 0
  }
  y = '      3.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_zloops_zloop_0():
  x = {
    'records': _records,
    'k_branch': 'zloops',
    'k_leaf': 'zloop',
    'record_index': 0
  }
  y = '  7.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_prices_apples_1():
  x = {
    'records': _records,
    'k_branch': 'prices',
    'k_leaf': 'apples',
    'record_index': 1
  }
  y = '   0.75'
  z = f(**x)
  return pxyz(x, y, z)

def t_prices_bananas_1():
  x = {
    'records': _records,
    'k_branch': 'prices',
    'k_leaf': 'bananas',
    'record_index': 1
  }
  y = '    1.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_applezzz_1():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'applezzz',
    'record_index': 1
  }
  y = '    4.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_bananazzz_1():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'bananazzz',
    'record_index': 1
  }
  y = '     5.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_pearzzzzzz_1():
  x = {
    'records': _records,
    'k_branch': 'volumes',
    'k_leaf': 'pearzzzzzz',
    'record_index': 1
  }
  y = '      6.00'
  z = f(**x)
  return pxyz(x, y, z)

def t_zloops_zloop_1():
  x = {
    'records': _records,
    'k_branch': 'zloops',
    'k_leaf': 'zloop',
    'record_index': 1
  }
  y = '  7.00'
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_prices_apples_0():      return pf('!t_prices_apples_0')
  if not t_prices_bananas_0():     return pf('!t_prices_bananas_0')
  if not t_volumes_applezzz_0():   return pf('!t_volumes_applezzz_0')
  if not t_volumes_bananazzz_0():  return pf('!t_volumes_bananazzz_0')
  if not t_volumes_pearzzzzzz_0(): return pf('!t_volumes_pearzzzzzz_0')
  if not t_zloops_zloop_0():       return pf('!t_zloops_zloop_0')
  if not t_prices_apples_1():      return pf('!t_prices_apples_1')
  if not t_prices_bananas_1():     return pf('!t_prices_bananas_1')
  if not t_volumes_applezzz_1():   return pf('!t_volumes_applezzz_1')
  if not t_volumes_bananazzz_1():  return pf('!t_volumes_bananazzz_1')
  if not t_volumes_pearzzzzzz_1(): return pf('!t_volumes_pearzzzzzz_1')
  if not t_zloops_zloop_1():       return pf('!t_zloops_zloop_1')
  return True
