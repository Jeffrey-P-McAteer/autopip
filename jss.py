
import os
import sys
import subprocess
import io
import traceback

pip_pkgs = '/tmp/jss-pip'
os.makedirs(pip_pkgs, exist_ok=True)
sys.path.append(pip_pkgs)

try:
  import json_stream
except:
  subprocess.run([
    sys.executable, '-m', 'pip', 'install', f'--target={pip_pkgs}', 'json-stream'
  ])
  import json_stream

import json

example_input = '''
{"name": "Dict 1", "num": 5}
{"name": "Dict Two", "num": 2}
{"name": "Dict 3", "num": 13}{"name": "Dict Four", "num": 44}
'''

file = io.StringIO()
file.write(example_input)
file.seek(0)

# ^ file is our stand-in for a pipe, but we assume moving backwards in the stream is impossible.

# for _ in range(0, 10):
#   try:
#     json_data = json_stream.load(file)

#     for d in json_data:
#       print(f'd = {d}')
#   except:
#     traceback.print_exc()



decoder = json.JSONDecoder()
decode_buffer = ''
num_errs = 0
while num_errs < 128:
  try:
    decoder = json.JSONDecoder()
    decode_buffer += file.read(1)
    #print(f'decode_buffer = {decode_buffer}')
    data,index = decoder.raw_decode(decode_buffer.strip())
    decode_buffer = '' # empty buffer
    print()
    print(f'data = {data}')
    print()
  except:
    #traceback.print_exc()
    num_errs += 1




