import sqlite3
from command_processing import update_user_points, add_user_to_database
def test_update_points():
    update_user_points('Balls', 70)
    print("Test update complete.")

def create_tables():
    conn = sqlite3.connect('points.db')  # Connect to the points.db database
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY
        )
    ''')
    
    # Create user_points table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_points (
            username TEXT PRIMARY KEY,
            points INTEGER NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_tables()
    add_user_to_database("Balls")
    test_update_points()
