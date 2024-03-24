
import os
import sys
import mmap
import threading
import time
import struct

def run_ipc_func(fn_name, *args):
  file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
  if not os.path.exists(file_name):
    raise Exception(f'{file_name} does not exist!')



r = run_ipc_func('http_get', 'http://example.org')

print(f'r = {r}')


r = run_ipc_func('http_get', 'http://1.1.1.1')

print(f'r = {r}')



