import csv
import mysql.connector
import requests

def create_table():
    # Drive link to the CSV file
    drive_link = "https://drive.google.com/uc?export=download&id=101P9quxHoMZMZCVWQ5o-shonk2lgK1-o"
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    # Define the table name
    table_name = "bq_results"
    create_table_query = f"""
    CREATE TABLE {table_name} ( 
        store_id VARCHAR(255),
        timezone_str VARCHAR(255)
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
            insert_query = f"INSERT INTO {table_name} VALUES ('{column1}','{column2}');"
            # Execute the insert query
            cursor.execute(insert_query)
    # enter the null values in timezone_str as 'America/Chicago'
    update_query = f"UPDATE {table_name} SET timezone_str='America/Chicago' where timezone_str is null);"
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