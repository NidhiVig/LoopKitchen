import csv
import mysql.connector
import requests

def create_table():
    # Drive link to the CSV file
    drive_link = "https://drive.google.com/uc?export=download&id=1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg"
    # MySQL database configuration
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    # Define the table name
    table_name = "menu_hours"
    create_table_query = f"""
    CREATE TABLE {table_name} (
        store_id VARCHAR(255),
        day INT,
        start_time_local TIME,
        end_time_local TIME
    );
    """
    # Execute the create table query
    cursor.execute(create_table_query)

    # Send a GET request to download the file
    response = requests.get(drive_link)

    # Create a temporary file to save the downloaded content
    with open("temp.csv", "wb") as file:
        file.write(response.content)

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
            column3 = row[2]
            column4 = row[3]
            insert_query = f"INSERT INTO {table_name} VALUES ('{column1}','{column2}','{column3}','{column4}');"
            # Execute the insert query
            cursor.execute(insert_query)
    # query to update the null values in start_time_local and end_time_local as 0:00:00 and 23:59:59 respectively
    update_query = f"UPDATE {table_name} SET start_time_local = '00:00:00', end_time_local = '23:59:59' WHERE start_time_local is null and end_time_local is null;"
    cursor.execute(update_query)
    # Remove the temporary file
    import os
    os.remove("temp.csv")
    # Commit the changes to the database
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
# create_table()