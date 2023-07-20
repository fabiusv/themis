import pydantic # type: ignore
from .Location import Location

class MetaData(pydantic.BaseModel):
  location: Location
  timezone: str
  language: str
  def encode(self):
    return {"location": self.location.encode(), "timezone": self.timezone, "language": self.language}
  @staticmethod
  def decode(meta_data_dict):
    return MetaData(location=Location.decode(meta_data_dict["location"]), timezone=meta_data_dict["timezone"], language=meta_data_dict["language"])