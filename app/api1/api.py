import json
import uuid
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None

    try:
        conn = sqlite3.connect("data.db")
        conn.execute(""" CREATE TABLE IF NOT EXISTS "geospatial_job" (job_id BLOB, type text, grid_file text, pole_file text, critical_distances BLOB, status text)""")
    except Error as e:
        print('error')

    return conn

def select_all_tasks():
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    conn = create_connection("data.db")
    conn = conn.cursor()
    conn.execute("SELECT * FROM geospatial_job")

    all_jobs = {}
    rows = conn.fetchall()
    n = 1
    print(rows)
    for row in rows:
        print(row)
        all_jobs["Job_",n] = row
        n = n+1
    return json.dumps(str(all_jobs))

create_connection("data.db")

def fetch_job_details():
    return select_all_tasks()

def get_job(job_id: str):
    try:
        job_details = {}
        # conn = sqlite3.connect('data.db', check_same_thread=False)
        conn = create_connection("data.db")
        conn = conn.cursor()
        sql_select_query = """select * from geospatial_job where job_id = ?"""
        conn.execute(sql_select_query, (job_id,))

        records = conn.fetchall()
        #row_value = conn.fetchone()

        for row in records:
             job_details['job_id'] = row[0]
             job_details['type'] = row[1]
             job_details['grid_file'] = row[2]
             job_details['pole_file'] = row[3]
             job_details['critical_distances'] = row[4]
             job_details['status'] = row[5]

        if len(records) == 0:
            job_details["Error"] = "Job ID not found: "+ job_id
            return json.dumps(job_details)
        else:
            return json.dumps(job_details)


    except sqlite3.Error as error:
        print("Failed to read data from table", error)

def create_job(payload):
    type = payload['type']
    grid_file = payload['grid_file']
    pole_file = payload['pole_file']
    critical_distances = payload['critical_distances']
    job_id = uuid.uuid1()
    validation_failed = False
    valid_err = {}
    job_id_res = {}

    job_id = str(job_id)
    if str(isinstance(type, str)):
        if type == "2D" or type == "3D":
            print("Type valid")
        else:
            valid_err["type"] = "Validation error: Type values can be 2D or 3D"
            validation_failed = True
    if grid_file.startswith("s3://"):
        print("grid_file valid")
    else:
        valid_err["grid_file"] = "Validation error: grid_file variable is valid s3 endpoint should start with s3://"
        validation_failed = True

    if pole_file.startswith("s3://"):
        print("grid_file valid")
    else:
        valid_err["pole_file"] = "Validation error: pole_file variable is valid s3 endpoint should start with s3://"
        validation_failed = True

    x = 0
    if any(int(y) > int(x) for y in critical_distances) and len(critical_distances) >= 3 and all([item.isdigit() for item in critical_distances]):
        print("critical_distances parameter valid")
    else:
        valid_err["critical_distances"] = "Validation Error: array of 3 integers > 0"
        validation_failed = True

    if validation_failed:
        return json.dumps(valid_err)

    # Add an entry to the db
    conn = sqlite3.connect('data.db', check_same_thread=False)
    conn.execute("INSERT INTO geospatial_job (job_id, type , grid_file, pole_file, critical_distances, status) VALUES (?,?,?,?,?,?)",(job_id, type, grid_file, pole_file, str(critical_distances), "Pending"))
    conn.commit()
    select_all_tasks()

    job_id_res["job_id"] = job_id
    return json.dumps(job_id_res)
