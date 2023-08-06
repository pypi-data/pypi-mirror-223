from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.many.values.detect_type import f as detect_type

f = lambda heading, values, type=None: {
  'heading': heading,
  'values': values,
  'type': type or detect_type(values)
}

def t_0():
  x = {'heading': 'abc', 'values': [0, 1, 2]}
  y = {'heading': 'abc', 'values': [0, 1, 2], 'type': 'int'}
  z = f(**x)
  return pxyz(x, y, z)

def t_1():
  x = {'heading': 'abc', 'values': [0, 1, 2], 'type': 'int'}
  y = {'heading': 'abc', 'values': [0, 1, 2], 'type': 'int'}
  z = f(**x)
  return pxyz(x, y, z)

def t():
  if not t_0(): return pf('!t_0')
  if not t_1(): return pf('!t_1')
  return True
