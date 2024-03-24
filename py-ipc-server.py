
import os
import sys
import mmap
import threading
import time
import struct
import traceback

file_name = os.environ.get('PATH_TO_MAPPED_FILE', '/tmp/ipc.bin')
print(f'Serving function calls sent to {file_name}')

MAP_SIZE = 16 * 1024
last_fn_nonce = 0
with open(file_name, 'ab+') as fd:
  fd.seek(0)
  fd.write(b'\x00' * MAP_SIZE )
  fd.flush()
  fd.seek(0)

  mm = mmap.mmap(fd.fileno(), MAP_SIZE)

  while True:
    try:
      if int(mm[0]) != last_fn_nonce:
        print(f'New incoming nonce = {int(mm[0])}')

        last_fn_nonce = int(mm[0])

    except:
      traceback.print_exc()
      if 'KeyboardInterrupt' in traceback.format_exc():
        break
      time.sleep(1)





