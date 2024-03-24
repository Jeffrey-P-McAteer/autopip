
# Duplicate of the giant string we call code in Program.cs

import sys
import os
import importlib
import importlib.abc
import subprocess
import tempfile
import traceback

# Does not load packages; instead, we install this as the first
# item in sys.meta_path and we install everything that
# can't be loaded using importlib.import_module() - careful of the recursion!
class AutoPipMetaFinder(importlib.abc.MetaPathFinder):
  def __init__(self):
    self.currently_recursing = False
    self.module_install_path = os.path.join(
      tempfile.gettempdir(),
      f'AutoPip_{sys.version_info.major}_{sys.version_info.minor}_site-packages'
    )
    os.makedirs(self.module_install_path, exist_ok=True)
    sys.path.insert(0, self.module_install_path)
    # Some python libs require searching out .exe files they execute
    module_bin_dir = os.path.join(self.module_install_path, 'bin')
    sys.path.append(module_bin_dir)
    os.environ['PATH'] = os.environ.get('PATH', '')+os.pathsep+module_bin_dir

  def find_spec(self, fullname, path, target=None):
    # print(f'self.currently_recursing={self.currently_recursing} find_spec({fullname}, {path}, {target})')
    try:
      if self.currently_recursing:
        return None # Do not recurse infinitely

      if fullname in ['sitecustomize', 'usercustomize'] or '.' in fullname:
        return None # Do not install system libs OR child libraries

      if fullname in sys.modules.keys():
        return None # Skip already-imported modules

      # Determine which line of code invoked us - if it's a folder under sys.path, always return None.
      # Some python libs do a try/except to see what's available, and it's good to not
      # dynamically install those libraries (like _decimal)
      stack = traceback.extract_stack(limit=48)
      formatted_stack = traceback.format_list(stack)
      line_called_from = (formatted_stack[0].split('\n')+['',''])[1].strip()

      if len(line_called_from) < 1 or not 'import ' in line_called_from.lower():
        return None # Not called by an import statement!

      # Also early exit IF there is anything from self.module_install_path in the stack trace,
      # as we do not want to break detailed module loaders from things like matplotlib
      for frame_txt in formatted_stack:
        if self.module_install_path in frame_txt:
          return None # Outta here! Let 3rd party libs manage their own sub-modules.


      # If there is a comment on the line, get all whitespace-deliminated words as tokens
      # and use those as PIP arguments
      pip_install_flags = []
      if '#' in line_called_from:
        comment_str = line_called_from.split('#', 1)[1].strip()
        pip_install_flags = comment_str.split()

      # Assume package name == module name and use that if no explicit comment found
      if len(pip_install_flags) < 1:
        pip_install_flags = [ fullname ]

      self.currently_recursing = True

      needs_install = False
      try:
        # m = importlib.import_module(fullname) # Causes re-import of many complex python libs, best avoid

        s = importlib.util.find_spec(fullname)
        if s is None:
          try:
            m = importlib.import_module(fullname)
            needs_install = False # no spec, but imported. Is likely builtin library, safe to re-import!
          except:
            #traceback.print_exc()
            needs_install = True
      except:
        #traceback.print_exc()
        needs_install = True

      self.currently_recursing = False

      if needs_install:
        pip_env = os.environ.copy()
        pip_env.pop('PYTHONPATH', None)
        subprocess.run([
          sys.executable, '-m', 'pip', 'install',
            f'--target={self.module_install_path}',
            *pip_install_flags
        ], env=pip_env, check=True)

      return None
    except:
      #traceback.print_exc()
      return None


sys.meta_path.insert(0, AutoPipMetaFinder())
