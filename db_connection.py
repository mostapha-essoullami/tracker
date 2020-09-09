import psycopg2

def create_connection():

    host = "gpstacker06.postgres.database.azure.com"
    dbname = "test"
    user = "gpsadmin@gpstacker06"
    password = "gpsTracker06"
    port="5432"
    sslmode = "require"

    # Construct connection string
    conn_string = f"dbname='{dbname}' user='{user}' host='{host}' password='{password}' port='{port}' sslmode='{sslmode}'"
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        return conn,cursor
    except:
        print ("unable to connect to the database")
        return 0