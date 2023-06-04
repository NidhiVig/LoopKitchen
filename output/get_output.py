import csv
import mysql.connector
import requests
import os
def get_available_filename(base_filename):
    # Check if the base filename exists
    if not os.path.exists(base_filename):
        return base_filename

    # If the base filename exists, generate new filenames by appending a number
    counter = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}{counter}.csv"
        if not os.path.exists(new_filename):
            return new_filename
        counter += 1
def get_output():
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    output_query = f"""
    
WITH uptime_hours AS (
select 
     ss.store_id,
     (TIMESTAMPDIFF(SECOND, min(timestamp_utc), max(timestamp_utc))/ 60) AS minutes
from store_status ss join menu_hours bq
on ss.store_id = bq.store_id
WHERE timestamp_utc >= ((select max(timestamp_utc) from store_status) - INTERVAL 1 hour) and status = 'active'
and (dayofweek(TIMESTAMP_UTC)-1)%7 = bq.day and (TIME(timestamp_utc)>=start_time_local and TIME(timestamp_utc)<=end_time_local)
group by ss.store_id,bq.store_id
    ),
uptime_last_day AS (
select
	ss.store_id,
	(TIMESTAMPDIFF(SECOND, min(timestamp_utc), max(timestamp_utc))/ 3600) AS hours
from store_status ss join menu_hours bq
on ss.store_id = bq.store_id
WHERE timestamp_utc >= ((select max(timestamp_utc) from store_status) - INTERVAL 1 day) and status = 'active'
and (dayofweek(TIMESTAMP_UTC)-1)%7 = bq.day and (TIME(timestamp_utc)>=start_time_local and TIME(timestamp_utc)<=end_time_local)
group by ss.store_id,bq.store_id
    ),
uptime_week AS (
select
	ss.store_id,
	(TIMESTAMPDIFF(SECOND, min(timestamp_utc), max(timestamp_utc))/ 3600) AS hours
from store_status ss join menu_hours bq
on ss.store_id = bq.store_id
WHERE timestamp_utc >= ((select max(timestamp_utc) from store_status) - INTERVAL 1 week) and status = 'active'
and (dayofweek(TIMESTAMP_UTC)-1)%7 = bq.day and (TIME(timestamp_utc)>=start_time_local and TIME(timestamp_utc)<=end_time_local)
group by ss.store_id,bq.store_id
    )
SELECT
    mh.store_id,
    uh.minutes 'uptime_last_hour(in minutes)',
    dc.hours 'uptime_last_day(in hours)',
    wc.hours 'uptime_last_week(in hours)',
    (60-uh.minutes) 'downtime_last_hour(in minutes)',
    (24-dc.hours) 'downtime_last_day(in hours)',
    (24*7-wc.hours) 'downtime_last_week(in hours)'
    FROM
    bq_results mh
    join
    uptime_hours uh ON mh.store_id = uh.store_id
    join
    uptime_last_day dc ON mh.store_id = dc.store_id
	join
    uptime_week wc ON mh.store_id = wc.store_id;
    """
    cursor.execute(output_query)
    rows = cursor.fetchall()

    # Define the path of the temporary CSV file
    temp_csv_file = get_available_filename('temp.csv')
    current_dir = os.path.abspath(os.path.dirname(__file__))
    print(current_dir)
    
    # Join the current directory path with the filename to get the absolute file path
    csv_location = os.path.join(current_dir, temp_csv_file)
    
    
    # Write the query result to the CSV file
    with open(temp_csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                         'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])  # Write the header row
        writer.writerows(rows)  # Write the query result rows to the CSV file

    # Close the database connection
    cursor.close()
    connection.close()

    # Return the path of the temporary CSV file
    return temp_csv_file


# get_output()