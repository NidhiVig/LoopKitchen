import mysql.connector

def drop_table():
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    table = ['store_status','menu_hours','bq_results']
    for i in table:
        drop_table_query = f"""
        DROP TABLE {i};
        """
        cursor.execute(drop_table_query)