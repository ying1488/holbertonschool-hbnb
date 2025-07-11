from app import create_app
import mysql.connector

app = create_app()

def run_sql_script(filename):
    # Setup your DB connection params - adjust as needed
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='hbnb_evo_2_db'
    )
    cursor = conn.cursor()
    with open(filename, 'r') as f:
        sql_script = f.read()
    
    # Split and execute statements one by one
    for statement in sql_script.split(';'):
        stmt = statement.strip()
        if stmt:
            cursor.execute(stmt)
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    # Run the SQL schema setup before starting app
    run_sql_script('app/hbnb_tables.sql')
    
    app.run(debug=True)
