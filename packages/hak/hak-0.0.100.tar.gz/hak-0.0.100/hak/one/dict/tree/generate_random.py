from random import random as u
from hak.one.string.char.random_az import f as u_az
from hak.one.string.print_and_return_false import f as pf
from hak.pxyz import f as pxyz
from hak.one.dict.is_a import f as is_dict

def f(v, decay=0.5):
  if u() <= v:
    v *= decay
    obj = {}
    while u() <= v:
      obj[u_az()] = f(v)
    return obj
  else:
    return {}

def t():
  x = {'v': 1, 'decay': 0.9}
  z = f(**x)
  return is_dict(z)
