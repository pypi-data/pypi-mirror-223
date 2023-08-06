from hak.one.dict.rate.to_str import f as rate_to_str
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.one.dict.rate.make import f as make_rate

# records_k_branch_k_leaf_to_leaf_values
def f(records, k_branch, k_leaf):
  z = [
    rate_to_str(r[k_branch][k_leaf])
    for r
    in records
  ]
  return z

def t_prices_apples():
  x = {
    'records': [
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
    ],
    'k_branch': 'prices',
    'k_leaf':   'apples'
  }
  y = ['0.25', '0.75']
  z = f(**x)
  return pxyz(x, y, z)

def t_prices_bananas():
  x = {
    'records': [
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
    ],
    'k_branch': 'prices',
    'k_leaf':   'bananas'
  }
  y = ['0.50', '1.00']
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_applezzz():
  x = {
    'records': [
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
    ],
    'k_branch': 'volumes',
    'k_leaf':   'applezzz'
  }
  y = ['1.00', '4.00']
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_bananazzz():
  x = {
    'records': [
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
    ],
    'k_branch': 'volumes',
    'k_leaf':   'bananazzz'
  }
  y = ['2.00', '5.00']
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes_pearzzzzzz():
  x = {
    'records': [
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
    ],
    'k_branch': 'volumes',
    'k_leaf':   'pearzzzzzz'
  }
  y = ['3.00', '6.00']
  z = f(**x)
  return pxyz(x, y, z)

def t_zloops_zloop():
  x = {
    'records': [
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
    ],
    'k_branch': 'zloops',
    'k_leaf':   'zloop'
  }
  y = ['7.00', '7.00']
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
