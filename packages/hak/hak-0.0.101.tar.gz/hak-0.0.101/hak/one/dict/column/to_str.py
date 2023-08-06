from datetime import date

from hak.one.dict.column.get_width import f as get_width
from hak.one.dict.column.make import f as make_column
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

def f(x):
  _w = get_width(x)
  w = _w + 2

  if   x['type'] == 'int': value_strings = [f" {v:>{_w}} " for v in x['values']]
  elif any([
    x['type'] == 'date',
    x['type'] == 'str'
  ]):
    _values = [str(v) for v in x['values']]
    value_strings = [f" {v:>{_w}} " for v in _values]
  else:
    raise TypeError(f"Unexpected type: {x['type']}")
    # value_strings = [f" {v:>{_w}} " for v in x['values']]
  
  return '\n'.join([
    '-'*w,
    f" {x['heading']:>{_w}} ",
    '-'*w,
    *value_strings,
    '-'*w,
  ])

def t_0():
  x = make_column('a', [0])
  y = '\n'.join([
    '---',
    ' a ',
    '---',
    ' 0 ',
    '---',
  ])
  z = f(x)
  return pxyz(x, '\n'+y, '\n'+z)

def t_1():
  x = make_column('abc', [0, 10, 23])
  y = '\n'.join([
    '-----',
    ' abc ',
    '-----',
    '   0 ',
    '  10 ',
    '  23 ',
    '-----',
  ])
  z = f(x)
  return pxyz(x, '\n'+y, '\n'+z)

def t_2():
  x = make_column('ab', [0, 100, 2300])
  y = '\n'.join([
    '------',
    '   ab ',
    '------',
    '    0 ',
    '  100 ',
    ' 2300 ',
    '------',
  ])
  z = f(x)
  return pxyz(x, '\n'+y, '\n'+z)

def t_date():
  x = make_column(
    'date',
    [date(2023, 1, 1), date(2023, 4, 8), date(2023, 12, 31)]
  )
  y = '\n'.join([
    '------------',
    '       date ',
    '------------',
    ' 2023-01-01 ',
    ' 2023-04-08 ',
    ' 2023-12-31 ',
    '------------',
  ])
  z = f(x)
  return pxyz(x, '\n'+y, '\n'+z)

def t_str():
  x = make_column(
    'animal',
    [
      'dog',
      'cat',
      'fox'
    ]
  )
  y = '\n'.join([
    '--------',
    ' animal ',
    '--------',
    '    dog ',
    '    cat ',
    '    fox ',
    '--------',
  ])
  z = f(x)
  return pxyz(x, '\n'+y, '\n'+z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  if not t_date(): return pf('!t_date')
  if not t_str(): return pf('!t_str')
  return True
