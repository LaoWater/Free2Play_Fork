import json
import psycopg2


def process_origin_nexus_dataset(value):
    side_control_l = 'Left '
    side_control_r = 'Right '
    if value < 0:
        side_control_l = 'Right '
        side_control_r = 'Left '

    sql_query = f"""
    SELECT nn.NexusName,
    CASE WHEN nml.OppositeSide = FALSE THEN '{side_control_r}' ELSE '{side_control_l}' END || m.MuscleName,
    CASE nml.Type WHEN 'Compression' THEN 'Release/Lengthen' ELSE 'Activate/Shorten' END
    FROM NexusMuscleLink nml
    INNER JOIN Muscles m ON m.MuscleID = nml.MuscleID
    INNER JOIN NexusNetwork nn ON nn.NexusID = nml.NexusID
    WHERE nn.NexusName = 'Origin Nexus'
    ORDER BY nn.NexusID, nml.OppositeSide, nml.Type DESC, m.MuscleID
    """
    query_database(sql_query)
    json_results = query_database_json(sql_query)
    return json_results


def process_nebula_nexus_dataset(value):
    side_control_l = 'Left '
    side_control_r = 'Right '
    if value < 0:
        side_control_l = 'Right '
        side_control_r = 'Left '

    sql_query = f"""
    SELECT nn.NexusName,
    CASE WHEN nml.OppositeSide = FALSE THEN '{side_control_r}' ELSE '{side_control_l}' END || m.MuscleName,
    CASE nml.Type WHEN 'Compression' THEN 'Release/Lengthen' ELSE 'Activate/Shorten' END
    FROM NexusMuscleLink nml
    INNER JOIN Muscles m ON m.MuscleID = nml.MuscleID
    INNER JOIN NexusNetwork nn ON nn.NexusID = nml.NexusID
    WHERE nn.NexusName = 'Nebula Nexus'
    ORDER BY nn.NexusID, nml.OppositeSide, nml.Type DESC, m.MuscleID
    """
    query_database(sql_query)
    json_results = query_database_json(sql_query)
    return json_results


def process_horizon_nexus_dataset(value):
    side_control_l = 'Left '
    side_control_r = 'Right '
    if value < 0:
        side_control_l = 'Right '
        side_control_r = 'Left '

    sql_query = f"""
    SELECT nn.NexusName,
    CASE WHEN nml.OppositeSide = FALSE THEN '{side_control_r}' ELSE '{side_control_l}' END || m.MuscleName,
    CASE nml.Type WHEN 'Compression' THEN 'Release/Lengthen' ELSE 'Activate/Shorten' END
    FROM NexusMuscleLink nml
    INNER JOIN Muscles m ON m.MuscleID = nml.MuscleID
    INNER JOIN NexusNetwork nn ON nn.NexusID = nml.NexusID
    WHERE nn.NexusName = 'Horizon Nexus'
    ORDER BY nn.NexusID, nml.OppositeSide, nml.Type DESC, m.MuscleID
    """
    query_database(sql_query)
    json_results = query_database_json(sql_query)
    return json_results


def connect_to_database():
    conn = psycopg2.connect(
        dbname="free2play",
        user="postgres",  # Change this to your PostgreSQL username if different
        password="postgres",  # Change this to your PostgreSQL password
        host="localhost"  # Change this if your PostgreSQL is hosted elsewhere
    )
    return conn


def query_database(query):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query)

    # Fetch and print each row
    for row in cursor.fetchall():
        print(row)

    print('\n')

    cursor.close()
    conn.close()


def query_database_json(query):
    conn = connect_to_database()
    cursor = conn.cursor()

    # Execute the query
    cursor.execute(query)

    # Initialize an empty list to store the results
    results = []

    # Fetch each row and append to the list as a dictionary
    for row in cursor.fetchall():
        result = {
            "Nexus": row[0],
            "Target Muscle": row[1],
            "Action": row[2]
        }
        results.append(result)

    # Convert the list of dictionaries to a JSON string
    json_results = json.dumps(results, indent=4)  # 'indent' for pretty-printing

    # Close the connection
    cursor.close()
    conn.close()

    return json_results


####################
# Main Query Start #
####################
# origin_json_results = process_origin_nexus_dataset(0.2)
# nebula_json_results = process_nebula_nexus_dataset(0.33)
# horizon_json_results = process_horizon_nexus_dataset(-0.21)
