using System;
using System.Diagnostics;

namespace AutoPip
{
    class Program
    {
        static void Main(string[] args)
        {
            ProcessStartInfo psi = new ProcessStartInfo("python");
            // psi.ArgumentList.Add("chaos.py");
            psi.Arguments = "chaos.py";

            var p = Process.Start(psi);
            p.WaitForExit();
        }
    }
}
