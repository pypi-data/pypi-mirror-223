# ignore_overlength_lines
from .to_horizontal_line import f as records_to_horizontal_line
from .to_k_branch_row import f as records_to_k_branch_row
from .to_sub_header_and_underline import f as records_to_sh
from .to_top_border import f as records_to_top_border
from .to_units_row_with_underline import f as records_to_units_row_with_underline
from .to_value_rows import f as records_to_value_rows
from datetime import date
from hak.one.dict.rate.make import f as make_rate
from hak.one.string.print_and_return_false import f as pf

f = lambda x: '\n'.join([
  records_to_top_border(x),
  records_to_k_branch_row(x),
  records_to_horizontal_line(x),
  *records_to_sh(x),
  *records_to_units_row_with_underline(x),
  *records_to_value_rows(x),
  records_to_horizontal_line(x)
])

def t_nested():
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
  y = '\n'.join([
    "|--------------------|-----------------------------------|--------|",
    "|             prices |                           volumes | zloops |",
    "|---------|----------|----------|-----------|------------|--------|",
    "|  apples |  bananas | applezzz | bananazzz | pearzzzzzz |  zloop |",
    "|---------|----------|----------|-----------|------------|--------|",
    "| $/apple | $/banana |    apple |    banana |       pear |  zloop |",
    "|---------|----------|----------|-----------|------------|--------|",
    "|    0.25 |     0.50 |     1.00 |      2.00 |       3.00 |   7.00 |",
    "|    0.75 |     1.00 |     4.00 |      5.00 |       6.00 |   7.00 |",
    "|---------|----------|----------|-----------|------------|--------|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t_date():
  x = [
    {
      'date': date(2023, 7, 27),
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
      'date': date(2023, 7, 28),
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
  y = '\n'.join([
    "|------------|--------------------|-----------------------------------|--------|",
    "|       date |             prices |                           volumes | zloops |",
    "|------------|---------|----------|----------|-----------|------------|--------|",
    "|            |  apples |  bananas | applezzz | bananazzz | pearzzzzzz |  zloop |",
    "|------------|---------|----------|----------|-----------|------------|--------|",
    "|            | $/apple | $/banana |    apple |    banana |       pear |  zloop |",
    "|------------|---------|----------|----------|-----------|------------|--------|",
    "| 2023-07-27 |    0.25 |     0.50 |     1.00 |      2.00 |       3.00 |   7.00 |",
    "| 2023-07-28 |    0.75 |     1.00 |     4.00 |      5.00 |       6.00 |   7.00 |",
    "|------------|---------|----------|----------|-----------|------------|--------|",
  ])
  z = f(x)
  return y == z or pf([f'x: {x}', f'y:\n{y}', f'z:\n{z}'])

def t():
  if not t_nested(): return pf('t_nested failed')
  # if not t_date(): return pf('t_date failed')
  return True
