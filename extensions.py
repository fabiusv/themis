def safe_list_get(l, idx):
  try:
    return l[idx]
  except IndexError:
    return None