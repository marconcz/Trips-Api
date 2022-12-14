from psycopg2 import connect
import src.repository.secret as secret

# use connect function to establish the connection
def get_con():
    conn = connect(host=secret.host,
            database=secret.database,
            user=secret.user,
            password=secret.password,
            port=secret.port
        )
    return conn

def bd_connection():
    try:
        conn = get_con()
        cursor = conn.cursor()
        # New comment 
        # Creating table as per requirement
        sql = '''CREATE TABLE IF NOT EXISTS TRIPSTABLE(TRIP_ID SERIAL PRIMARY KEY,
										DRIVER_ID VARCHAR(255),
										CLIENT_ID VARCHAR(255) NOT NULL,
									    PRICE NUMERIC,
                                        STATUS VARCHAR(20),
                                        LONGITUDE FLOAT,
                                        LATITUDE FLOAT,
                                        DEST_LONGITUDE FLOAT,
                                        DEST_LATITUDE FLOAT,
                                        DRIVER_LONGITUDE FLOAT,
                                        DRIVER_LATITUDE FLOAT,
                                        DRIVER_SCORE INTEGER check (DRIVER_SCORE BETWEEN  1 and 5),
                                        CLIENT_SCORE INTEGER check (CLIENT_SCORE BETWEEN  1 and 5),
                                        STARTING_POINT VARCHAR(100),
                                        DESTINATION_POINT VARCHAR(100))'''
        cursor.execute(sql)
        print("Table created successfully........")
        conn.commit()
        
        # Closing the connection
        conn.close()


        #print("Connection with Heroku_DDBB is OK")
    except Exception as error:
        print(error)

#When a driver complete a trip it marks its trip id completed
def trip_completed(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()

        sql = """UPDATE tripstable
                    SET status = 'completed'
                    WHERE trip_id = '{0}' and status = 'running';""".format(trip_id)
        cursor.execute(sql)
        conn.commit()
        result = cursor.statusmessage
        if (result == "UPDATE 1"):
            result = "completed"
        else:
            result = "Failed updating"

        return result
    except Exception as error:
        print(error)

# init a trip setting its status to Running
def init_trip(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()
        # New comment 
        # Creating table as per requirement
        sql = """UPDATE tripstable
                            SET status = 'running'
                            WHERE trip_id = '{0}' and status = 'accepted';""".format(trip_id)
        cursor.execute(sql)
        conn.commit()
        result = cursor.statusmessage
        if (result == "UPDATE 1"):
            result = "Running"
        else:
            result = "Failed updating"
        # Closing the connection
        conn.close()
        return result

        #print("Connection with Heroku_DDBB is OK")
    except Exception as error:
        print(error)
#Get trip status
def get_trip_status(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()
        # New comment 
        # Creating table as per requirement
        sql = '''SELECT status FROM tripstable \
            WHERE trip_id = {0}'''.format(trip_id)
        cursor.execute(sql)
        return cursor.fetchone()[0]
        # Closing the connection
        conn.close()


        #print("Connection with Heroku_DDBB is OK")
    except Exception as error:
        print(error)
#Register a trip with a client when trip´s accepted, without driver
def register_trip(client_id: str, price: float, user_lat: float, user_long: float, dest_lat: float, dest_long: float, starting: str, destination: str):
    try:
        conn = get_con()
        cursor = conn.cursor()

        postgres_search_client_trips_query = """SELECT * FROM Tripstable\
                                                WHERE client_id='{0}' and
                                                      status<>'completed';""".format(client_id)
        cursor.execute(postgres_search_client_trips_query)
        if cursor.rowcount > 0:
            return "User have other trips waiting or in progress"
        postgres_insert_query = """INSERT INTO TripsTable(trip_id,\
                                                            client_id,\
                                                            price,\
                                                            status,\
                                                            latitude,\
                                                            longitude,\
                                                            dest_latitude,\
                                                            dest_longitude,\
                                                            starting_point,\
                                                            destination_point)\
                                VALUES(DEFAULT,'{0}','{1}','waiting','{2}','{3}','{4}','{5}','{6}','{7}')\
                                RETURNING trip_id;""".format(client_id,price,user_lat,user_long,dest_lat,dest_long,starting,destination)
        cursor.execute(postgres_insert_query)
        conn.commit()
        trip_id = cursor.fetchone()[0]
        return trip_id
    except Exception as error:
        print("Error:",error)
        return "An error occurred"
    finally:
    # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
#
def get_driver_pos(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()

        postgres_select_query = """SELECT driver_latitude FROM TripsTable\
                                    WHERE trip_id={0};""".format(trip_id)
        cursor.execute(postgres_select_query)
        result = [cursor.fetchone()]
        postgres_select_query = """SELECT driver_longitude FROM TripsTable\
                                    WHERE trip_id={0};""".format(trip_id)
        cursor.execute(postgres_select_query)
        result.append(cursor.fetchone())

    except Exception as error:
        print("Error:",error)
        return "An error occurred"
    finally:
    # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
        return result
#
def get_driver(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()

        postgres_insert_query = """SELECT driver_id FROM TripsTable\
                                    WHERE trip_id={0};""".format(trip_id)
        cursor.execute(postgres_insert_query)
        driver_id = cursor.fetchone()[0]
        if (cursor.rowcount == 1 and driver_id is not None):
            result = 'driver_found'
        else:
            result = 'not_found'
        conn.commit()
  
    except Exception as error:
        print("Error:",error)
        return "An error occurred"
    finally:
    # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
        return result
#
def search_trip_without_driver(trip_id):
    try:
        conn = get_con()
        cursor = conn.cursor()

        postgres_insert_query = """SELECT
                                    trip_id, price, latitude, longitude, dest_latitude, dest_longitude
                                    FROM    TripsTable
                                    WHERE   driver_id IS NULL and
									        status = 'waiting' and
                                            trip_id <> {0}
                                    LIMIT 1;""".format(trip_id)
        cursor.execute(postgres_insert_query)
        conn.commit()
        result = cursor.fetchone()
        if (cursor.rowcount == 1):
            return result #Return 1 row in cursor rows
        else:
            return "Failed: No trips available to do"
    except Exception as error:
        print("Error:",error)
        return "An error occurred"
    finally:
    # closing database connection.
        if conn:
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")
#
def update_pos(trip_id, driver_lat: float, driver_long: float):
    try:
        connection = get_con()
        cursor = connection.cursor()
        # Update single record now
        sql_update_query = """UPDATE tripstable
                                SET driver_longitude = '{1}',
                                    driver_latitude = '{2}'
                                WHERE trip_id = '{0}';""".format(trip_id, driver_long, driver_lat)
        cursor.execute(sql_update_query)
        
        connection.commit()
        
        return cursor.statusmessage
    except Exception as error:
        print("Error in update operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
#
def register_driver(trip_id, driver_id: str, driver_lat: float, driver_long: float):
    try:
        connection = get_con()
        cursor = connection.cursor()
        # Update single record now
        sql_update_query = """UPDATE tripstable
                                SET driver_id = '{0}',
	                                status = 'accepted',
                                    driver_longitude = '{2}',
                                    driver_latitude = '{3}'
                                WHERE trip_id = '{1}' and status = 'waiting';""".format(driver_id,trip_id, driver_long, driver_lat)
        cursor.execute(sql_update_query)
        
        connection.commit()
        return cursor.rowcount
    except Exception as error:
        print("Error in update operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
 
#Method to debug TripsTable
def check():
    try:
        connection = get_con()
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from TripsTable"
 
        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from publisher table using cursor.fetchall")
        publisher_records = cursor.fetchall()
 
        print("Print each row and it's columns values")
        for row in publisher_records:
            print("Id = ", row[0], )
            print("driver = ", row[1])
            print("client  = ", row[2], "\n")

    except Exception as error:
        print("Error while fetching data from PostgreSQL", error)
    finally:
    # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
def trip_qualify(trip_id, user_id, score):
    try:
        connection = get_con()
        cursor = connection.cursor()
        # search trip
        postgres_select_query = """SELECT
                                    driver_id, client_id, driver_score, client_score
                                    FROM    TripsTable
                                    WHERE   trip_id = {0} and status = 'completed';""".format(trip_id)
        cursor.execute(postgres_select_query)
        row = cursor.fetchone()
        print(row)
        if (row[0] == user_id and (row[3] is None)):
            user_qualified = "client_score"
        elif(row[1] == user_id and (row[2] is None)):
            user_qualified = "driver_score"
        else:
            return 'failed: score can not be overwrited'
        print(user_qualified)
        sql_update_query = """UPDATE tripstable
                                SET {0} = '{2}'
                                WHERE trip_id = '{1}' and status = 'completed';""".format(user_qualified, trip_id, score)
        print(sql_update_query)
        cursor.execute(sql_update_query)

        result = 'failed'
        if (cursor.rowcount == 1):
            result = 'updated'
        connection.commit()


        return result
    except Exception as error:
        print("Error in update operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_score_average(user_id):
    try:
        connection = get_con()
        cursor = connection.cursor()    
        postgres_select_query = """SELECT driver_id, client_id 
                                    FROM tripstable
                                    WHERE (driver_id = '{0}' or client_id = '{0}')
                                          and status = 'completed'
                                    LIMIT 1;""".format(user_id)
        cursor.execute(postgres_select_query)
        row = cursor.fetchone()

        if (row[1] == user_id):
            user_score = "client_score"
            user_type = "client_id"
        elif(row[0] == user_id):
            user_score = "driver_score"
            user_type = "driver_id"
        else:
            return 0

        postgres_average_query = """SELECT AVG({0})
                                    FROM tripstable
                                    WHERE {1} = '{2}';""".format(user_score, user_type, user_id)
        cursor.execute(postgres_average_query)
        
        return cursor.fetchone()[0]


    except Exception as error:
        print("Error in select operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def get_trip_history(user_id):
    try:
        connection = get_con()
        cursor = connection.cursor()    
        postgres_select_query = """SELECT (starting_point, destination_point)
                                    FROM tripstable
                                    WHERE client_id = '{0}'
                                          and status = 'completed'
                                    ORDER BY trip_id
                                    LIMIT 5;""".format(user_id)
        cursor.execute(postgres_select_query)

        if (cursor.rowcount >= 1):
            return cursor.fetchall()
        else:
            return None

    except Exception as error:
        print("Error in select operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def cancel_a_trip(trip_id):
    try:
        connection = get_con()
        cursor = connection.cursor()    
        postgres_delete_query = """DELETE FROM tripstable
                                     WHERE trip_id = '{0}' 
                                     and status = 'waiting';""".format(trip_id)
        cursor.execute(postgres_delete_query)
        if (cursor.statusmessage == "DELETE 1"):
            connection.commit()
            return "deleted"
        else:
            return "Trips does not exist"

    except Exception as error:
        print("Error in SQL operation", error)
    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")