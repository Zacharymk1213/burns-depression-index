import sqlite3
from datetime import datetime

def calculate_burns_score(responses):
    """
    Calculate total score from array of 25 responses
    Each response should be between 0-4
    """
    if len(responses) != 25:
        raise ValueError("Must provide exactly 25 responses")
        
    if not all(isinstance(x, int) and 0 <= x <= 4 for x in responses):
        raise ValueError("All responses must be integers between 0 and 4")
        
    return sum(responses)

def get_depression_level(score):
    """
    Return depression level based on total score
    """
    if 0 <= score <= 5:
        return "No Depression"
    elif 6 <= score <= 10:
        return "Normal but unhappy"
    elif 11 <= score <= 25:
        return "Mild depression"
    elif 26 <= score <= 50:
        return "Moderate depression"
    elif 51 <= score <= 75:
        return "Severe depression"
    elif 76 <= score <= 100:
        return "Extreme depression"
    else:
        return "Invalid score"

def init_db():
    """
    Initialize SQLite database and create table if it doesn't exist
    """
    conn = sqlite3.connect('burns_checklist.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS checklist_entries
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
         score INTEGER NOT NULL,
         depression_level TEXT NOT NULL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    ''')
    conn.commit()
    conn.close()

def save_score(score):
    """
    Save score to database with current timestamp
    Returns the entry ID
    """
    conn = sqlite3.connect('burns_checklist.db')
    c = conn.cursor()
    
    depression_level = get_depression_level(score)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    c.execute('''
        INSERT INTO checklist_entries (score, depression_level, timestamp)
        VALUES (?, ?, ?)
    ''', (score, depression_level, current_time))
    
    entry_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return entry_id

def get_all_entries():
    """
    Retrieve all entries from database
    """
    conn = sqlite3.connect('burns_checklist.db')
    c = conn.cursor()
    c.execute('SELECT * FROM checklist_entries ORDER BY timestamp DESC')
    entries = c.fetchall()
    conn.close()
    return entries

# Initialize database when module is imported
init_db()

# Example usage:
if __name__ == "__main__":
    # Example responses (25 numbers between 0-4)
    sample_responses = [2, 1, 0, 2, 1, 3, 2, 1, 0, 2, 1, 0, 2, 1, 3, 
                       2, 1, 0, 2, 1, 0, 2, 1, 0, 0]
    
    # Calculate score
    score = calculate_burns_score(sample_responses)
    print(f"Total Score: {score}")
    print(f"Depression Level: {get_depression_level(score)}")
    
    # Save to database
    entry_id = save_score(score)
    print(f"Saved entry with ID: {entry_id}")
    
    # Retrieve all entries
    entries = get_all_entries()
    print("\nAll entries:")
    for entry in entries:
        print(f"ID: {entry[0]}, Score: {entry[1]}, Level: {entry[2]}, Time: {entry[3]}")
