using System;
using System.Diagnostics;
using System.IO;

namespace AutoPip
{
    class Program
    {
        // Returns string path to sitecusomize module
        public static string CreatePython_sitecustomize() {
          string tmp_dir = Path.GetTempPath();
          string tmp_sitecustomize_py = tmp_dir+Path.DirectorySeparatorChar+"sitecustomize.py";
          File.WriteAllText(tmp_sitecustomize_py, @"
print('Hello sitecustomize!')

");
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
