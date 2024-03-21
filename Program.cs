using System;
using System.Diagnostics;
using System.IO;

namespace AutoPip
{
    class Program
    {
        // Returns string path to sitecusomize module
        public static string CreatePython_sitecustomize() {
          string tmp_dir = Path.GetTempPath().TrimEnd(Path.DirectorySeparatorChar);
          string tmp_sitecustomize_py = tmp_dir+Path.DirectorySeparatorChar+"sitecustomize.py";
          File.WriteAllText(tmp_sitecustomize_py, @"
import sys
import os
import importlib
import importlib.abc
import importlib.machinery

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

  def find_spec(self, fullname, path, target=None):

    if fullname in ['sitecustomize', 'usercustomize'] or '.' in fullname:
      return None # Do not install system libs OR child libraries

    if self.currently_recursing:
      return None # Do not recurse infinitely

    if fullname in sys.modules.keys():
      return None # Skip already-imported modules

    # Determine which line of code invoked us - if it's a folder under sys.path, always return None.
    # Some python libs do a try/except to see what's available, and it's good to not
    # dynamically install those libraries (like _decimal)
    stack = traceback.extract_stack(limit=48)
    line_called_from = traceback.format_list(stack)[0].split('\n')[1].strip()

    # print(f'line_called_from = {line_called_from}')

    if len(line_called_from) < 1 or not 'import ' in line_called_from.lower():
      return None # Not called by an import statement!

    # If there is a comment on the line, get all whitespace-deliminated words as tokens
    # and use those as PIP arguments
    pip_install_flags = []
    if '#' in line_called_from:
      comment_str = line_called_from.split('#', 1)[1].strip()
      pip_install_flags = comment_str.split()

    # Assume package name == module name and use that if no explicit comment found
    if len(pip_install_flags) < 1:
      pip_install_flags = [ fullname ]

    # print(f'find_spec({fullname}, {path}, {target})')

    self.currently_recursing = True

    needs_install = False
    try:
      _ = importlib.import_module(fullname)
    except:
      needs_install = True

    self.currently_recursing = False

    if needs_install:
      pip_env = os.environ.copy()
      pip_env['PYTHONPATH'] = ''
      subprocess.run([
        sys.executable, '-m', 'pip', 'install',
          f'--target={self.module_install_path}',
          *pip_install_flags
      ], env=pip_env, check=True)

    return None


sys.meta_path.insert(0, AutoPipMetaFinder())


".Trim());
          return tmp_sitecustomize_py;
        }
        public static void Main(string[] args)
        {
            string sitecustomize_location = CreatePython_sitecustomize();
            Console.WriteLine($"sitecustomize_location = {sitecustomize_location}");

            ProcessStartInfo psi = new ProcessStartInfo("python");
            // psi.ArgumentList.Add("chaos.py");
            psi.Arguments = "chaos.py";
            psi.EnvironmentVariables.Add("PYTHONPATH",
                Environment.GetEnvironmentVariable("PYTHONPATH")+Path.PathSeparator+
                Path.GetDirectoryName(sitecustomize_location)
            );

            var p = Process.Start(psi);
            p.WaitForExit();
        }
    }
}
