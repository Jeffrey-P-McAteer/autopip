
import os
import sys
import mmap
import threading
import time
import ctypes

# This structure MUST be identical across sending + recieving processes
class SharedStruct(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('message_num',  ctypes.c_uint), # Both sides must increment message_num, on fn call + on fn return
        ('fn_name',      ctypes.c_char * 128 ),              # Up to 128 chars func name
        ('fn_args',      ctypes.c_char * (16 * 1024) ),      # Pass up to 16kb of arguments, which will be interpreted as into a list of N \x00-terminated strings
        ('return_items', ctypes.c_char * (128 * 1024 * 1024) ),  # Return up to 128mb, which will be interpreted as into a list of N \x00-terminated strings
    ]

    def field_size(self, field_name):
      for f_name, field_type in self._fields_:
        if f_name == field_name:
          return ctypes.sizeof(field_type)
      raise Exception(f'Cannot find field {field_name}!')

MAP_SIZE = ctypes.sizeof(SharedStruct)

def run_ipc_func(fn_name, *args):
  file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
  if not os.path.exists(file_name):
    raise Exception(f'{file_name} does not exist!')
  with open(file_name, 'ab+') as fd:
    mm = mmap.mmap(fd.fileno(), MAP_SIZE)
    mm_struct = SharedStruct.from_buffer(mm)

    mm_struct.fn_name = fn_name.encode('utf-8')
    # TODO \x00-join
    mm_struct.fn_args = (' '.join([str(x) for x in args])).encode('utf-8')

    # Inform server func is available
    our_nonce = (mm_struct.message_num + 1) % 1024
    mm_struct.message_num = our_nonce
    while mm_struct.message_num == our_nonce:
      time.sleep(0.05)

    # TODO parse
    return mm_struct.return_items.decode('utf-8')



r = run_ipc_func('http_get', 'http://example.org')

print(f'r = {r}')


r = run_ipc_func('http_get', 'http://ifconfig.me')

print(f'r = {r}')



