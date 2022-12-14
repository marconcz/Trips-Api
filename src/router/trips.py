# Third party imports
from unittest import result
from fastapi import APIRouter 
#Our imports
from src.repository.trips_bbdd import *

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
async def accept_client_trip(client_id: str, price: float,user_lat: float,user_long: float,dest_lat: float, dest_long: float, starting_name: str, destination_name: str):
    operation = register_trip(client_id, price, user_lat,user_long,dest_lat, dest_long, starting_name, destination_name)
    return {"trip_id": operation} 

#If a driver is looking for doing a trip
@router.get("/search-trip/{trip_id}")
async def search_trip(trip_id):
    operation = search_trip_without_driver(trip_id)
    if (operation != "Failed: No trips available to do"): #Failed searching a trip (no one available)
        return {"trip_id": operation[0], "trip_price": operation[1], "lat": operation[2], "long": operation[3],\
            "dest_lat": operation[4], "dest_long": operation[5]}
    else:
        return {'status': operation}

#If a driver is looking for accept a trip
@router.post("/accept-driver-trip")
async def accept_driver_trip(trip_id, driver_id: str, driver_lat: float, driver_long: float):
    record = register_driver(trip_id, driver_id, driver_lat, driver_long)
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

#A driver needs to update his position
@router.put("/driver/position")
async def update_position(trip_id, driver_lat: float, driver_long: float):
    row_updated = update_pos(trip_id, driver_lat, driver_long)
    return {"updated": row_updated}

# A client looking for driver position
@router.get("/trip-driver-position")
async def get_driver_position(trip_id):
    position = get_driver_pos(trip_id)
    return {"position_lat": position[0][0],"position_long": position[1][0]}

#A client want trip status = "Running" or "waiting" (for driver)
@router.get("/trip")
async def get_trip(trip_id):
    return {"trip_status": get_trip_status(trip_id)}

# Init a Trip by setting status on "Running" from driver device
@router.put("/init")
async def init(trip_id):
    result = init_trip(trip_id)
    return {"trip_updated_to": result}

#If a client answer about a driver was found
@router.post("/trip/finish/{trip_id}")
async def finish_trip(trip_id):
    record = trip_completed(trip_id)
    return {"trip_status": record}

#Qualify: A user wants qualify a trip
@router.post("/trip/{trip_id}/qualify/{user_id}/score/{score}")
async def trip_qualification(trip_id, user_id, score):
    record = trip_qualify(trip_id, user_id, score)
    return {"status": record}

#Return score average
@router.get("/score/{user_id}")
async def get_score(user_id):
    return {"score": get_score_average(user_id)}

#Return last user trips
@router.get("/trips/history/{user_id}")
async def get_history(user_id):
    return {"history": get_trip_history(user_id)}

@router.psot("trip/canceled/{trip_id}")
async def calcel_trip(trip_id):
    return {"status": cancel_a_trip(trip_id)}