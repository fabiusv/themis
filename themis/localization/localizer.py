from .local_strings import local_strings
from fastapi import HTTPException
def get_localization(lang_code):
  result = local_strings.get(lang_code)
  if result:
    return result
  else:
    raise HTTPException(status_code=404, detail="Language ID not found")