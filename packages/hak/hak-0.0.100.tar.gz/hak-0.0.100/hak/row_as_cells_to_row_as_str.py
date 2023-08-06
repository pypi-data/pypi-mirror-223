from hak.many.strings.to_table_row import f as cell_strings_to_table_row_string
from hak.pxyz import f as pxyz
from hak.one.string.print_and_return_false import f as pf

# f_s
# row_as_cells_to_row_as_str
f = lambda x: cell_strings_to_table_row_string(x, ' ')

def t_a():
  x = ['   0.25', '    0.50', '    1.00', '     2.00', '      3.00', '  7.00']
  y = '|    0.25 |     0.50 |     1.00 |      2.00 |       3.00 |   7.00 |'
  z = f(x)
  return pxyz(x, y, z)

def t_b():
  x = ['   0.75', '    1.00', '    4.00', '     5.00', '      6.00', '  7.00']
  y = '|    0.75 |     1.00 |     4.00 |      5.00 |       6.00 |   7.00 |'
  z = f(x)
  return pxyz(x, y, z)

def t():
  if not t_a(): return pf('!t_a')
  if not t_b(): return pf('!t_b')
  return True
