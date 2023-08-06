from hak.many.strings.to_table_row import f as cell_strings_to_table_row_string
from hak.pxyz import f as pxyz

# cell_lines_to_row_line
f = lambda x: cell_strings_to_table_row_string(x, '-')

def t():
  x = ['-------', '--------', '--------', '---------', '----------', '------']
  y = '|---------|----------|----------|-----------|------------|--------|'
  z = f(x)
  return pxyz(x, y, z)
