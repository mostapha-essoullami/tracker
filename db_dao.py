import psycopg2
import db_connection

def insert_data(imei , longitud , latitud ,vitesse, time_tracking ):
    try:
        conn,cursor = db_connection.create_connection()
    except:
        return
    if cursor!=None:
        try:
            cursor.execute("INSERT INTO track (imie,logitude ,latitude ,vitesse,DATE) VALUES (%s,%s,%s,%s,%s);", (imei , longitud , latitud ,vitesse, time_tracking))
            conn.commit()
        except:
            print("can't add data to database'")
            return 0
        finally:
            cursor.close()
            conn.close()
