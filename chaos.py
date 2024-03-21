
import json5

print(f'json5 = {json5}')

# From https://matplotlib.org/stable/gallery/lines_bars_and_markers/simple_plot.html
# matplotlib is a good test of our "installer", as it comes with native code + calls executables on the PATH
if False:
  import matplotlib.pyplot as plt
  import numpy as np

  print(f'plt = {plt}')
  print(f'np = {np}')


  # Data for plotting
  t = np.arange(0.0, 2.0, 0.01)
  s = 1 + np.sin(2 * np.pi * t)

  fig, ax = plt.subplots()
  ax.plot(t, s)

  ax.set(xlabel='time (s)', ylabel='voltage (mV)',
         title='About as simple as it gets, folks')
  ax.grid()

  fig.savefig("test.png")
  plt.show()


from PIL import Image # pillow

print(f'PIL.Image = {Image}')

