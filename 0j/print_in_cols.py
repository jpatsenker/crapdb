# print a list-like object in the given number of cols, each
# output line has the optional third string prepended

import types, sys

def print_in_cols(thing, ncols, prepend = "") :
  if type(thing) == types.DictType :
    list = thing.items()
  elif type(thing) == types.ListType or type(thing) == types.TupleType :
    list = thing
  else :
    print thing
    return
  i = 1
  listlen = len(list)
  for item in list :
    print item,
    if i == listlen :
      # sys.stdout.write("\n")
      return
    if i % ncols == 0 :
      sys.stdout.write(",\n%s" % prepend)
    else :
      sys.stdout.write(", ")
    i = i + 1 
