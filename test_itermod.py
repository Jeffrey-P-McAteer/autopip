
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import python_iterator_module

print(f'python_iterator_module = {python_iterator_module}')

for item in python_iterator_module.yield_items():
  print(f'item = {item}')

print('Done!')

