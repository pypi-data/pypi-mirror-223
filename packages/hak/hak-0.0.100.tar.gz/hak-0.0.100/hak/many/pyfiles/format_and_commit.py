from hak.one.system.git.push_after_delay import f as push_commits_after_delay
from hak.many.strings.filepaths.py.get import f as list_py_files
from hak.many.strings.pyfiles.filter_out_items import f as filter_out_items
from hak.many.pyfiles.format import f as auto_format_py_filenames

def f(_L_pi, fn_a=auto_format_py_filenames, fn_b=push_commits_after_delay):
  a = fn_a(_L_pi)
  b = fn_b(5)
  return a, b

t = lambda: f(list('abc'), lambda x: x, lambda x: x)==(list('abc'), 5)

if __name__ == '__main__':
  f(
    filter_out_items(
      list_py_files(),
      [
        './haki.pyfiles.format_and_commit.py',
        # './data.py',
        # './_auto_format_one.py',
        # './src/x_contains_run_function.py',
        # './src/x_contains_test_function.py',
        # './src/data.py',
        # './src/auto_format_one.py',
      ]
    )
  )
