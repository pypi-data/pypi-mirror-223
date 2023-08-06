from hak.pxyz import f as pxyz
from hak.one.string.print_and_return_false import f as pf

f = lambda cell_strings, col_separator_char: (
  f'|{col_separator_char}'+
  f'{col_separator_char}|{col_separator_char}'.join(cell_strings)+
  f'{col_separator_char}|'
)

def t_0():
  x = {
    'cell_strings': [
      '------------------',
      '---------------------------------',
      '------'
    ],
    'col_separator_char': '-'
  }
  y = '|--------------------|-----------------------------------|--------|'
  z = f(**x)
  return pxyz(x, y, z)

def t_1():
  x = {
    'cell_strings': [
      '            prices',
      '                          volumes',
      'zloops'
    ],
    'col_separator_char': ' '
  }
  y = '|             prices |                           volumes | zloops |'
  z = f(**x)
  return pxyz(x, y, z)

def t_2():
  x = {
    'cell_strings': [
      '-------',
      '--------',
      '--------',
      '---------',
      '----------',
      '------'
    ],
    'col_separator_char': '-'
  }
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(**x)
  return pxyz(x, y, z)

def t_3():
  x = {
    'cell_strings': [
      ' apples',
      ' bananas',
      'applezzz',
      'bananazzz',
      'pearzzzzzz',
      ' zloop'
    ],
    'col_separator_char': ' '
  }
  y = '|  apples |  bananas | applezzz | bananazzz | pearzzzzzz |  zloop |'
  z = f(**x)
  return pxyz(x, y, z)

def t_4():
  x = {
    'cell_strings': [
      '-------',
      '--------',
      '--------',
      '---------',
      '----------',
      '------'
    ],
    'col_separator_char': '-'
  }
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(**x)
  return pxyz(x, y, z)

def t_5():
  x = {
    'cell_strings': [
      '$/apple',
      '$/banana',
      '   apple',
      '   banana',
      '      pear',
      ' zloop'
    ],
    'col_separator_char': ' '
  }
  y = '| $/apple | $/banana |    apple |    banana |       pear |  zloop |'
  z = f(**x)
  return pxyz(x, y, z)

def t_6():
  x = {
    'cell_strings': [
      '-------',
      '--------',
      '--------',
      '---------',
      '----------',
      '------'
    ],
    'col_separator_char': '-'
  }
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(**x)
  return pxyz(x, y, z)

def t_7():
  x = {
    'cell_strings': [
      '   0.25',
      '    0.50',
      '    1.00',
      '     2.00',
      '      3.00',
      '  7.00'
    ],
    'col_separator_char': ' '
  }
  y = '|    0.25 |     0.50 |     1.00 |      2.00 |       3.00 |   7.00 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_8():
  x = {
    'cell_strings': [
      '   0.75',
      '    1.00',
      '    4.00',
      '     5.00',
      '      6.00',
      '  7.00'
    ],
    'col_separator_char': ' '
  }
  y = '|    0.75 |     1.00 |     4.00 |      5.00 |       6.00 |   7.00 |'
  z = f(**x)
  return pxyz(x, y, z)

def t_9():
  x = {
    'cell_strings': [
      '-------',
      '--------',
      '--------',
      '---------',
      '----------',
      '------'
    ],
    'col_separator_char': '-'
  }
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  if not t_2(): return pf('!t_2')
  if not t_3(): return pf('!t_3')
  if not t_4(): return pf('!t_4')
  if not t_5(): return pf('!t_5')
  if not t_6(): return pf('!t_6')
  if not t_7(): return pf('!t_7')
  if not t_8(): return pf('!t_8')
  if not t_9(): return pf('!t_9')
  return True
