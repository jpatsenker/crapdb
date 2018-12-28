#!/usr/bin/env python

'''
This function implements the (misnamed but very useful) ksh utility
type which, given an application name and the user's PATH, returns
the application's pathname or ""
The list of directories given by PATH has been extended to
include PYTHON_PATH (via sys.path)
'''

import posix, posixpath, sys, string

def find_cmd(name) :
  if posix.environ.has_key("PATH") :
    pathlist = string.split(posix.environ["PATH"], ":") + ["."]
  else :
    pathlist = ["."]
  pathlist = pathlist + sys.path
  # This covers the case where an absolute path has been given!
  if posixpath.isfile(name) :
    return(name)
  for p in pathlist :
    if posixpath.isfile(p + "/" + name) :
      return(p + "/" + name)
  return(None)


if __name__ == "__main__" :
  if len(sys.argv) != 2 :
    sys.stderr.write("Usage: %s <commmand>\n" % sys.argv[0])
    sys.exit(0)

  full_path = find_cmd(sys.argv[1])
  if full_path != None:
    print full_path
  else:
    print sys.argv[1] + " not found"
