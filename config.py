import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'yourusername'),
    'password': os.getenv('DB_PASS', 'yourpassword'),
    'database': os.getenv('DB_NAME', 'srijyothi_db')
}
