
import os
import sys
import mmap
import threading
import time
import struct
import traceback
import ctypes

import urllib
import urllib.request


file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
print(f'Serving function calls sent to {file_name}')

# This structure MUST be identical across sending + recieving processes
class SharedStruct(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ('message_num', ctypes.c_uint), # Both sides must increment message_num, on fn call + on fn return
        ('fn_name', ctypes.c_char * 128 ),              # Up to 128 chars func name
        ('fn_args', ctypes.c_char * (8 * 1024) ),       # Pass up to 8kb of arguments, which will be interpreted as into a list of N \x00-terminated strings
        ('return_items', ctypes.c_char * (8 * 1024) ),  # Return up to 8kb, which will be interpreted as into a list of N \x00-terminated strings
    ]

    def field_size(self, field_name):
      for f_name, field_type in self._fields_:
        if f_name == field_name:
          return ctypes.sizeof(field_type)
      raise Exception(f'Cannot find field {field_name}!')


def http_get(url_s):
  if not isinstance(url_s, str):
    url_s = url_s.decode('utf-8')
  with urllib.request.urlopen(url_s) as response:
    return response.read()


MAP_SIZE = ctypes.sizeof(SharedStruct)
last_fn_nonce = 0

# Zero file in write mode
with open(file_name, 'wb+') as fd:
  fd.write(b'\x00' * MAP_SIZE )
  fd.flush()

# Open in "append mode" and pass to mmap
with open(file_name, 'ab+') as fd:
  mm = mmap.mmap(fd.fileno(), MAP_SIZE)
  mm_struct = SharedStruct.from_buffer(mm)
  while True:
    try:
      if mm_struct.message_num == last_fn_nonce:
        continue

      print(f'New incoming nonce = {mm_struct.message_num}')

      print(f'  fn_name = {mm_struct.fn_name.decode("utf-8")}')
      print(f'  fn_args = {mm_struct.fn_args}')
      # print(f'  return_items = {mm_struct.return_items}')

      fn_args_arr = []
      for args_byte_s in mm_struct.fn_args.split(b'\x00'):
        if len(args_byte_s) > 0:
          fn_args_arr.append( args_byte_s.decode('utf-8') )

      if mm_struct.fn_name.decode("utf-8") == 'http_get':
        mm_struct.return_items = http_get(*fn_args_arr)[0:mm_struct.field_size('return_items')]
      else:
        mm_struct.return_items = b'\x00' * mm_struct.field_size('return_items')

      # Clear input values
      mm_struct.fn_name = b'\x00' * mm_struct.field_size('fn_name')
      mm_struct.fn_args = b'\x00' * mm_struct.field_size('fn_args')

      # Finally indicate return data has been written
      last_fn_nonce = (mm_struct.message_num + 1) % 1024
      mm_struct.message_num = last_fn_nonce

    except:
      traceback.print_exc()
      if 'KeyboardInterrupt' in traceback.format_exc():
        break
      time.sleep(1)

      # Clear _all_ values on exception!
      mm_struct.fn_name = b'\x00' * mm_struct.field_size('fn_name')
      mm_struct.fn_args = b'\x00' * mm_struct.field_size('fn_args')
      mm_struct.return_items = b'\x00' * mm_struct.field_size('return_items')

      # Remember to increment anyway so other process does not halt
      last_fn_nonce = (mm_struct.message_num + 1) % 1024
      mm_struct.message_num = last_fn_nonce





