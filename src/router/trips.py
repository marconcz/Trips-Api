# Third party imports
from unittest import result
from fastapi import APIRouter 
#Our imports
from src.repository.trips_bbdd import bd_connection,register_trip,check,register_driver

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
async def accept_client_trip(client_id: str):
    operation = register_trip(client_id)
    return {"status": operation} 

#If a driver is looking for doing a trip
@router.post("/accept-driver-trip")
async def accept_driver_trip(trip_id, driver_id: str):
    operation = register_driver(trip_id, driver_id)
    return {"status": operation}

#Debug method to check DD.BB structure
@router.get("/check-db")
async def check_database():
    check()
    return {}
