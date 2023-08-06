# ignore_overlength_lines
from hak.pxyz import f as pxyz
from hak.one.dict.get_sorted_keys import f as get_sorted_keys
from hak.one.string.print_and_return_false import f as pf
from hak.one.dict.rate.make import f as make_rate
from datetime import date

# records_k_branch_to_sorted_leaf_keys
# f = lambda records, field_name: get_sorted_keys(records[0][field_name])
def f(records, field_name):
  y = get_sorted_keys(records[0][field_name])
  return y

def t_prices():
  x = {
    'records': [
      {
        'prices': {
          'apples': make_rate(1, 4, {'$': 1, 'apple': -1}),
          'bananas': make_rate(1, 2, {'$': 1, 'banana': -1}),
        },
        '...': {}
      },
      {
        'prices': {
          'apples': make_rate(3, 4, {'$': 1, 'apple': -1}),
          'bananas': make_rate(1, 1, {'$': 1, 'banana': -1}),
        },
        '...': {}
      }
    ],
    'field_name': 'prices'
  }
  y = ['apples', 'bananas']
  z = f(**x)
  return pxyz(x, y, z)

def t_volumes():
  x = {
    'records': [
      {
        '...': {},
        'volumes': {
          'applezzz': make_rate(1, 1, {'apple': 1}),
          'bananazzz': make_rate(2, 1, {'banana': 1}),
          'pearzzzzzz': make_rate(3, 1, {'pear': 1})
        },
        '...': {}
      }, 
      {
        '...': {},
        'volumes': {
          'applezzz': make_rate(4, 1, {'apple': 1}),
          'bananazzz': make_rate(5, 1, {'banana': 1}),
          'pearzzzzzz': make_rate(6, 1, {'pear': 1})
        },
        '...': {}
      }
    ],
    'field_name': 'volumes'
  }
  y = ['applezzz', 'bananazzz', 'pearzzzzzz']
  z = f(**x)
  return pxyz(x, y, z)

def t_zloops():
  x = [
    {
      '...': {},
      'zloops': {'zloop': make_rate(7, 1, {'zloop': 1})}
    }, 
    {
      '...': {},
      'zloops': {'zloop': make_rate(7, 1, {'zloop': 1})}
    }
  ]
  a = 'zloops'
  y = ['zloop']
  z = f(x, a)
  return pxyz(x, y, z)

def t_date():
  x = {
    'records': [
      {'date': date(2023, 7, 27), 'prices': {'apples': {'numerator': 1, 'denominator': 4, 'unit': {'$': 1, 'apple': -1}}, 'bananas': {'numerator': 1, 'denominator': 2, 'unit': {'$': 1, 'banana': -1}}}, 'volumes': {'applezzz': {'numerator': 1, 'denominator': 1, 'unit': {'apple': 1}}, 'bananazzz': {'numerator': 2, 'denominator': 1, 'unit': {'banana': 1}}, 'pearzzzzzz': {'numerator': 3, 'denominator': 1, 'unit': {'pear': 1}}}, 'zloops': {'zloop': {'numerator': 7, 'denominator': 1, 'unit': {'zloop': 1}}}}, 
      {'date': date(2023, 7, 28), 'prices': {'apples': {'numerator': 3, 'denominator': 4, 'unit': {'$': 1, 'apple': -1}}, 'bananas': {'numerator': 1, 'denominator': 1, 'unit': {'$': 1, 'banana': -1}}}, 'volumes': {'applezzz': {'numerator': 4, 'denominator': 1, 'unit': {'apple': 1}}, 'bananazzz': {'numerator': 5, 'denominator': 1, 'unit': {'banana': 1}}, 'pearzzzzzz': {'numerator': 6, 'denominator': 1, 'unit': {'pear': 1}}}, 'zloops': {'zloop': {'numerator': 7, 'denominator': 1, 'unit': {'zloop': 1}}}}
    ],
    'field_name': 'date'
  }
  y = ['zloop']
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_prices(): return pf('!t_prices')
  if not t_volumes(): return pf('!t_volumes')
  if not t_zloops(): return pf('!t_zloops')
  # if not t_date(): return pf('!t_date')
  return True
