import csv
import mysql.connector
import requests

def create_table():
    # Drive link to the CSV file
    drive_link = "https://drive.google.com/uc?id=1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025&export=download&confirm=t&uuid=857f8f55-2287-46ab-adfe-75eda4a17d03"
    # MySQL database configuration
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    # Define the table name
    table_name = "store_status"
    create_table_query = f"""
    CREATE TABLE {table_name} (
        store_id VARCHAR(255),
        status VARCHAR(255) CHECK (status IN ('active', 'inactive')),
        timestamp_utc TIMESTAMP
    );
    """
    # Execute the create table query
    cursor.execute(create_table_query)

    # Send a GET request to download the file
    # response = requests.get(drive_link)

    # # Create a temporary file to save the downloaded content
    # with open("temp.csv", "wb") as file:
    #     file.write(response.content)

    # Open the CSV file
    with open("temp.csv", "r") as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)
        # Skip the first line
        next(csv_reader)
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Access individual columns in each row
            column1 = row[0]
            column2 = row[1]
            temp = row[2]
            column3 = temp[0:-4:]
            insert_query = f"INSERT INTO {table_name} VALUES ('{column1}','{column2}','{column3}');"
            # Execute the insert query
            cursor.execute(insert_query)
    # Remove the temporary file
    import os
    os.remove("temp.csv")
    # Commit the changes to the database
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
# create_table()