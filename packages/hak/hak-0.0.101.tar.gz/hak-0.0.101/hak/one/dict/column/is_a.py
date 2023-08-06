from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.one.dict.is_a import f as is_dict

f = lambda x: is_dict(x) and all([
  'heading' in x.keys(),
  'values' in x.keys(),
  'type' in x.keys(),
  len(x.keys()) == 3
])

def t_true():
  x = {'heading': 'abc', 'type': 'int', 'values': [0, 1, 2]}
  y = True
  z = f(x)
  return pxyz(x, y, z)

def t_false_none():
  x = None
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_zero():
  x = 0
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_one():
  x = 1
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_str():
  x = 'abc'
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_dict():
  x = {'...': '...'}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t_false_extra_key():
  x = {'heading': 'abc', 'values': [0, 1, 2], 'type': 'int', 'extra': None}
  y = False
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_true(): return pf('!t_true')
  if not t_false_none(): return pf('!t_false_none')
  if not t_false_zero(): return pf('!t_false_zero')
  if not t_false_one(): return pf('!t_false_one')
  if not t_false_str(): return pf('!t_false_str')
  if not t_false_dict(): return pf('!t_false_dict')
  if not t_false_extra_key(): return pf('!t_false_extra_key')
  return True
