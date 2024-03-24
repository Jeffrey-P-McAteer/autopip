
import os
import sys
import mmap
import threading
import time


file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
print(f'Serving function calls sent to {file_name}')

if not os.path.exists(file_name):
  with open(file_name, 'wb') as fd:
    fd.write(b'\0' * (16 * 1024) )

last_fn_nonce = 0
with open(file_name, 'rw+b') as fd:
  mm = mmap.mmap(fd.fileno(), 0)
  while True:
    try:
      if int.from_bytes(mm[0]) != last_fn_nonce:
        print(f'New incoming nonce = {int.from_bytes(mm[0])}')

        last_fn_nonce = int.from_bytes(mm[0])

    except:
      traceback.print_exc()
      if 'KeyboardInterrupt' in traceback.format_exc():
        break
      time.sleep(1)





