import csv
import mysql.connector
import requests

def get_output():
    connection = mysql.connector.connect(host='localhost',password='ramanujan45',user='root',database='loop_kitchen')
    cursor = connection.cursor()
    output_query = f"""
    WITH hourly_counts AS (
    SELECT
        store_id,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS uptime_last_hour,
        SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) AS downtime_last_hour
    FROM store_status
    WHERE timestamp_utc >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 WEEK)
    GROUP BY store_id
    ),
    daily_counts AS (
    SELECT
        store_id,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS uptime_last_day,
        SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) AS downtime_last_day
    FROM store_status
    WHERE timestamp_utc >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)
    GROUP BY store_id
    ),
    weekly_counts AS (
    SELECT
        store_id,
        SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS uptime_last_week,
        SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) AS downtime_last_week
    FROM store_status
    WHERE timestamp_utc >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 WEEK)
    GROUP BY store_id
    )
    SELECT
    mh.store_id,
    COALESCE(hc.uptime_last_hour, 0) AS uptime_last_hour,
    COALESCE(dc.uptime_last_day, 0) AS uptime_last_day,
    COALESCE(wc.uptime_last_week, 0) AS uptime_last_week,
    COALESCE(hc.downtime_last_hour, 0) AS downtime_last_hour,
    COALESCE(dc.downtime_last_day, 0) AS downtime_last_day,
    COALESCE(wc.downtime_last_week, 0) AS downtime_last_week
    FROM
    menu_hours mh
    LEFT JOIN
    hourly_counts hc ON mh.store_id = hc.store_id
    LEFT JOIN
    daily_counts dc ON mh.store_id = dc.store_id
    LEFT JOIN
    weekly_counts wc ON mh.store_id = wc.store_id
    JOIN
    bq_results br ON mh.store_id = br.store_id
    ORDER BY
    mh.store_id;
    """
    cursor.execute(output_query)
    rows = cursor.fetchall()

    # Define the path of the temporary CSV file
    temp_csv_file = 'temp.csv'

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

    # Call the function to retrieve the output and store it in a temporary CSV file
    # temp_csv_file_path = get_output()
get_output()