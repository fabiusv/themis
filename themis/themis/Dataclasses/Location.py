import pydantic

class Location(pydantic.BaseModel):
    lat: float
    lng: float
    def encode(self):
        return {"lat": self.lat, "lng": self.lng}
    @staticmethod
    def decode(location_dict):
        return Location(lat=location_dict["lat"], lng=location_dict["lng"])