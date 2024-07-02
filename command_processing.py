import sqlite3

def parse_command(text):
    # Handle /CCP adduser <username>
    if text.startswith("/CCP adduser"):
        parts = text.split()
        if len(parts) == 3:
            command, action, user = parts
            if action == "adduser":
                return {"action": "adduser", "user": user}
    
    # Handle /CCP listall
    elif text.startswith("/CCP listall"):
        return {"action": "listall"}
    
    # Handle /CCP gloriousleader
    elif text.startswith("/CCP gloriousleader"):
        return {"action": "gloriousleader"}
    
    # Handle /CCP help
    elif text.startswith("/CCP help"):
        return {"action": "help"}
    
    # Handle /CCP <username> <points>
    elif text.startswith("/CCP"):
        parts = text.split()
        if len(parts) == 3:
            command, user, points_str = parts
            try:
                points = int(points_str)
                return {"action": "update_points", "user": user, "points": points}
            except ValueError:
                return {"error": "Invalid points value"}

def process_command(command_data):
    action = command_data.get("action")
    
    if action == "gloriousleader":
        return print_leader()
    
    if action == "help":
        return print_help()

    if action == "adduser":
        user = command_data.get("user")
        result = add_user_to_database(user)
        return f"User {user} has been added." if result else f"Failed to add user {user}. It may already exist."
    
    elif action == "update_points":
        user = command_data.get("user")
        points = command_data.get("points")
        if points is not None:
            success, total_points = update_user_points(user, points)
            return f"{points} points updated for user {user}. Total points: {total_points}." if success else f"Failed to update points for user {user}."
        else:
            return "Error: Invalid points value."
        
    elif action == "listall":
        return list_users_and_scores()
    
    elif "error" in command_data:
        return command_data["error"]
    
    return "Invalid action"

def print_leader():
    return "ATTENTION CITIZEN This is the Central Intelligentsia of the Chinese Communist Party Glory to the CCP"

def print_help():
    return """
    CCP COMMAND HELP:
    
    /CCP adduser <NAME>
    /CCP <NAME> <POINTS>
    /CCP listall
    /CCP gloriousleader
    """


def add_user_to_database(username):
    conn = sqlite3.connect('points.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username,))
        conn.commit()
        print(f"User {username} successfully added.")
        return True
    except sqlite3.IntegrityError:
        print(f"User {username} already exists.")
        return False
    except Exception as e:
        print(f"Exception: {e}")
        return False
    finally:
        conn.close()

def update_user_points(username, points_to_add):
    conn = sqlite3.connect('points.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE username=?", (username,))
        if cursor.fetchone()[0] == 0:
            print(f"User {username} does not exist.")
            return False, 0

        cursor.execute("SELECT points FROM user_points WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            current_points = result[0]
            new_points = current_points + points_to_add
        else:
            new_points = points_to_add

        cursor.execute("INSERT OR REPLACE INTO user_points (username, points) VALUES (?, ?)", (username, new_points))
        conn.commit()
        return True, new_points
    except Exception as e:
        print(f"Exception: {e}")
        return False, 0
    finally:
        conn.close()

def list_users_and_scores():
    conn = sqlite3.connect('points.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            SELECT u.username, COALESCE(up.points, 0) as points
            FROM users u
            LEFT JOIN user_points up ON u.username = up.username
        ''')
        rows = cursor.fetchall()
        
        if not rows:
            return "No users found."
        
        result = "User Scores:\n"
        for row in rows:
            username, points = row
            result += f"{username}: {points} points\n"
        
        return result.strip()
    except Exception as e:
        print(f"Exception: {e}")
        return "Failed to retrieve user scores."
    finally:
        conn.close()
