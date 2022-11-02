# Third party imports
from unittest import result
from fastapi import APIRouter 
#Our imports
from src.repository.trips_bbdd import bd_connection, get_driver,register_trip,check,register_driver, search_trip_without_driver

# Define constants
PRICE_PER_KILOMETER = 5

# A dummy-client
client_id = "soyuncliente1234"

router = APIRouter()


@router.get("/")
async def main_route():
    bd_connection()
    return {"message": "Hey, It is me fastapi"}

#Example: Received travel distance
#Return: Trip price calculated with distance multiplied PRICE_PER_KILOMETER
@router.get("/trip-price")
async def price_calculator(distance: float):
    return {"price": PRICE_PER_KILOMETER*distance}

#When a Client accept the travel´s price, we save the travel ID
#in a postgreSQL database waiting for a driver
@router.post("/accept-client-trip")
async def accept_client_trip(client_id: str, price: float):
    operation = register_trip(client_id, price)
    return {"trip_id": operation} 

#If a driver is looking for doing a trip
@router.get("/search-trip")
async def search_trip():
    operation = search_trip_without_driver()
    return {"trip_id": operation[0], "price": operation[1]}

#If a driver is looking for accept a trip
@router.post("/accept-driver-trip")
async def accept_driver_trip(trip_id, driver_id: str):
    record = register_driver(trip_id, driver_id)
    return {"status": record}

#If a client answer about a driver was found
@router.post("/driver")
async def check_driver_status(trip_id):
    record = get_driver(trip_id)
    return {"driver_status": record}   

#Debug method to check DD.BB structure
@router.get("/check-db")
async def check_database():
    check()
    return {}
