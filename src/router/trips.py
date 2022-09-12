# Third party imports
from fastapi import APIRouter 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
geolocator = Nominatim(user_agent="fiuber")
# Define constants
PRICE_PER_KILOMETER = 5

router = APIRouter()


@router.get("/")
async def main_route():
    return {"message": "Hey, It is me fastapi"}

#Example: Transform an Address into Coordinates (Latitude, Longitude)
@router.get("/destination/address")
async def destination_with_address(address: str):
    location = geolocator.geocode(address)
    return {"latitude": location.latitude,"longitude": location.longitude}
#Example: Received Coordinates (Latitude, Longitude)
#Return: Distance(geodesic) between Coordinates received
@router.get("/price")
async def price_calculator(latitude: float, longitude: float, latitude2: float, longitude2: float):
    return {"price": PRICE_PER_KILOMETER*(geodesic((latitude,longitude),(latitude2,longitude2)).kilometers)}
