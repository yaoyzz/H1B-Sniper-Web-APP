

import psycopg2

def generate_query(search_term):
    # Create a database connection
    conn = psycopg2.connect(database="your_database_name", user="your_user_name", password="your_password", host="your_host", port="your_port")
    cur = conn.cursor()
    
    # Construct the SQL query based on the user input
    query = f"""
        SELECT job.job_title AS job_title, 
               job.full_time_position AS full_time_position, 
               employer.employer_name AS employer_name, 
               employer.employer_state AS employer_state, 
               employer.employer_city AS employer_city, 
               wage.wage_rate_of_pay_from AS wage_rate_of_pay_from, 
               wage.wage_unit_of_pay AS wage_unit_of_pay, 
               others.h_1b_dependent AS h_1b_dependent, 
               "case".case_status AS case_status, 
               "case".decision_date AS decision_date
        FROM job
        INNER JOIN employer ON job.case_number = employer.case_number
        INNER JOIN wage ON job.case_number = wage.case_number
        INNER JOIN others ON job.case_number = others.case_number
        INNER JOIN "case" ON job.case_number = "case".case_number
        WHERE job.job_title ILIKE '%{search_term}%' 
              OR employer.employer_name ILIKE '%{search_term}%' 
              OR employer.employer_city ILIKE '%{search_term}%' 
              OR employer.employer_state ILIKE '%{search_term}%';
    """
    
    # Execute the query
    cur.execute(query)
    
    # Fetch the results and print them out
    results = cur.fetchall()
    for row in results:
        print(row)
    
    # Close the database connection
    cur.close()
    conn.close()
