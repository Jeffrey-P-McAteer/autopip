
import os
import sys
import mmap
import threading
import time
import struct

MAP_SIZE = 16 * 1024

def run_ipc_func(fn_name, *args):
  file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
  if not os.path.exists(file_name):
    raise Exception(f'{file_name} does not exist!')
  with open(file_name, 'ab+') as fd:
    mm = mmap.mmap(fd.fileno(), MAP_SIZE)

    # TODO write func name + arguments

    # Increase nonce after writing func call data
    mm[0] = (int(mm[0]) + 1) % 255


r = run_ipc_func('http_get', 'http://example.org')

print(f'r = {r}')


r = run_ipc_func('http_get', 'http://1.1.1.1')

print(f'r = {r}')



