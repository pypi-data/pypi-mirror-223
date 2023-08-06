# ignore_overlength_lines
from ..k_branch.to_branch_col_width import f as get_top_head_width
from ..to_first_record_sorted_keys import f as get_K
from ..to_pad_k_branch import f as records_to_pad_k_branch
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

# records_and_fn_to_fn_applied_to_sorted_keys_of_records
f = lambda records, fn_a: [fn_a(records, k) for k in get_K(records)]

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
  x = {'records': _records, 'fn_a': get_top_head_width}
  y = [18, 33, 6]
  z = f(**x)
  return pxyz(x, y, z)

def t_1():
  x = {'records': _records, 'fn_a': records_to_pad_k_branch}
  y = ['            prices', '                          volumes', 'zloops']
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  return True
