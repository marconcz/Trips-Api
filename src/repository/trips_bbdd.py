from psycopg2 import connect
import src.repository.secret as secret

# use connect function to establish the connection
def bd_connection():
    try:
        conn = connect(host=secret.host,
            database=secret.database,
            user=secret.user,
            password=secret.password,
            port=secret.port
        )
        cursor = conn.cursor()
             
        # Creating table as per requirement
        sql = '''CREATE TABLE IF NOT EXISTS TripsTable(
                    trip_id SERIAL PRIMARY KEY,
                    driver_id VARCHAR(255),
                    client_id VARCHAR(255) NOT NULL
        )'''
        cursor.execute(sql)
        print("Table created successfully........")
        conn.commit()
        
        # Closing the connection
        conn.close()


        #print("Connection with Heroku_DDBB is OK")
    except Exception as error:
        print(error)
#Register a trip with a client when trip´s accepted, without driver
def register_trip(client_id: str):
    try:
        conn = connect(host=secret.host,
            database=secret.database,
            user=secret.user,
            password=secret.password,
            port=secret.port
        )
        cursor = conn.cursor()

        postgres_insert_query = """INSERT INTO TripsTable(trip_id,client_id)\
                                VALUES(DEFAULT,'{0}');""".format(client_id)
        cursor.execute(postgres_insert_query)
        conn.commit()
        return cursor.rowcount
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
def register_driver(trip_id, driver_id: str):
    try:
        connection = connect(host=secret.host,
            database=secret.database,
            user=secret.user,
            password=secret.password,
            port=secret.port
        )
        cursor = connection.cursor()
        # Update single record now
        sql_update_query = """Update TripsTable set \
                            driver_id = '{0}' where trip_id = '{1}'""".format(driver_id,trip_id)
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
        connection = connect(host=secret.host,
            database=secret.database,
            user=secret.user,
            password=secret.password,
            port=secret.port
        )
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