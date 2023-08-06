from hak.one.dict.column.make import f as make_column
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz

f = lambda x: max(len(x['heading']), *[len(str(v)) for v in x['values']])

def t_heading_dominant():
  x = make_column('abc', [0, 1, 2, 3])
  y = 3
  z = f(x)
  return pxyz(x, y, z)

def t_values_dominant():
  x = make_column('a', [0, 1000, 2, 3])
  y = 4
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_heading_dominant(): return pf('!t_heading_dominant')
  if not t_values_dominant(): return pf('!t_values_dominant')
  return True
