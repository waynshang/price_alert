def get_keys(x):
  if type(x) == list:
    map_keys = map(lambda y: list(y.keys())[0], x)
    return list(map_keys)
  else:
    return list(x.keys())

def get_values(x):
  if type(x) == list:
    map_keys = map(lambda y: list(y.values())[0], x)
    return list(map_keys)
  else:
    return list(x.values())

def create_dict_from_variables(keys, values):
  d = {}
  for index, key in enumerate(keys):
    d[key] = values[index]
  return d
