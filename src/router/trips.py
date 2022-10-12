# Third party imports
from fastapi import APIRouter 
from fastapi.encoders import jsonable_encoder
#from service.price_rules import driver, passenger, trip, rule
from fastapi.encoders import jsonable_encoder
# Define constants
PRICE_PER_KILOMETER = 5
#Global Variable RULE


router = APIRouter()


@router.get("/")
async def main_route():
    return {"message": "Hey, It is me fastapi"}

#Example: Transform an Address into Coordinates (Latitude, Longitude)
# @router.get("/destination-address")
# async def destination_with_address(address: str):
#     location = geolocator.geocode(address)
#     return {"latitude": location.latitude,"longitude": location.longitude}

#Example: Received travel distance
#Return: Trip price calculated with distance multiplied PRICE_PER_KILOMETER
@router.get("/trip-price")
async def price_calculator(distance: float):
    return {"price": PRICE_PER_KILOMETER*distance}
#


#Example: Receiver (passenger_stats, driver_stats, trip_stats)
#Return: Trip price@router.get("/trip-price")
# @router.post("/trip-price-with-rules")
# async def price_calculator(driver_stats: driver, client_stats: passenger, trip_stats: trip):
#     price = rule({driver.json()}).calculate_price()

#     return {"price": price}