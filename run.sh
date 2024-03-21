#!/bin/bash


# Stolen utilities from https://stackoverflow.com/a/56133028
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

shopt -s expand_aliases
set -e

# IMPORTANT: make sure dotnet is present in PATH before the next lines

# prepare csc alias

DOTNETDIR=$(dirname $(dirname $(dotnet --info | grep "Base Path" | cut -d' ' -f 6)))
CSCPATH=$(find $DOTNETDIR -name csc.dll -print | sort | tail -n1)
NETSTANDARDPATH=$(find $DOTNETDIR -path '*sdk/*/ref/netstandard.dll' '!' -path '*NuGetFallback*' -print | sort | tail -n1)

alias csc='dotnet $CSCPATH /r:$NETSTANDARDPATH '

# prepare csc_run alias

if [ ! -w "$DOTNETDIR" ]; then
  mkdir -p $HOME/.dotnet
  DOTNETDIR=$HOME/.dotnet
fi

DOTNETCSCRUNTIMECONFIG=$DOTNETDIR/csc-console-apps.runtimeconfig.json

alias csc_run='dotnet exec --runtimeconfig $DOTNETCSCRUNTIMECONFIG '

if [ ! -f $DOTNETCSCRUNTIMECONFIG ]; then
  DOTNETRUNTIMEVERSION=$(dotnet --list-runtimes |
    grep Microsoft\.NETCore\.App | tail -1 | cut -d' ' -f2)

  cat << EOF > $DOTNETCSCRUNTIMECONFIG
{
  "runtimeOptions": {
    "framework": {
      "name": "Microsoft.NETCore.App",
      "version": "$DOTNETRUNTIMEVERSION"
    }
  }
}
EOF
fi

csc     -out:Program.exe Program.cs
csc_run Program.exe


