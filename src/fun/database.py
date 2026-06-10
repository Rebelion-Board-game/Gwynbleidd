# src/database.py
import os
import time
import sys
from dotenv import load_dotenv
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row

# Load environment variables from the .env file
load_dotenv()

# Fetch from environment variables. If they don't exist, it evaluates to None or raises an error.
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Double-check that critical environment variables are actually loaded
if not all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("CRITICAL ERROR: Missing one or more database environment variables in .env file!")

# Build the connection string
DB_CONN_STRING = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD}"

# Initialize a global connection pool
# min_size=5 means it keeps 5 connections always ready. max_size=20 lets it expand under heavy load.
db_pool = ConnectionPool(
    conninfo=DB_CONN_STRING,
    min_size=5,
    max_size=20,
    open=False, # Don't open immediately, wait for FastAPI startup event
    kwargs={"row_factory": dict_row} # Automatically returns results as dictionaries
)

def init_db():
    """Initializes core system tables on startup. No game entries are created here."""
    for i in range(10):
        try:
            # Temporarily open the pool just to run migrations
            db_pool.open()
            
            with db_pool.connection() as conn:
                with conn.cursor() as cursor:
                    # 1. Core Users Table (Game Developers)
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS users (
                            id SERIAL PRIMARY KEY,
                            email VARCHAR(150) UNIQUE NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # 2. Core Games Table (Created only when dev requests it)
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS games (
                            id SERIAL PRIMARY KEY,
                            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                            game_name VARCHAR(100) NOT NULL,
                            current_users INT DEFAULT 0,
                            max_users INT DEFAULT 100,
                            api_key VARCHAR(255) UNIQUE NOT NULL,
                            api_secret VARCHAR(255) UNIQUE NOT NULL,
                            require_auth BOOLEAN DEFAULT FALSE,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    
                    # 3. Leaderboards Table (Holds scores linked to specific games)
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS leaderboards (
                            id SERIAL PRIMARY KEY,
                            game_id INTEGER REFERENCES games(id) ON DELETE CASCADE,
                            player_name VARCHAR(100) NOT NULL,
                            register_player_id INT DEFAULT NULL,
                            score INTEGER NOT NULL,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)

                    # 4. Players Table (Holds player's accounts)
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS players (
                            id SERIAL PRIMARY KEY,
                            game_id INTEGER NOT NULL REFERENCES games(id) ON DELETE CASCADE,
                            username VARCHAR(50) NOT NULL,
                            password_hash VARCHAR(255) NOT NULL,
                            last_login TIMESTAMP WITH TIME ZONE DEFAULT NULL,
                            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        
                            CONSTRAINT unique_game_player UNIQUE (game_id, username)
                        );
                    """)
                    conn.commit()
            
            print("PostgreSQL connection pool initialized and tables verified successfully.")
            return
        except KeyboardInterrupt:
            logging.info("Application stop Ctrl+C")
            sys.exit(0)
        except Exception as e:
            print(f"Waiting for PostgreSQL database to start... ({e})")
            time.sleep(2)
            
    raise Exception("Failed to connect to PostgreSQL database via connection pool.")


def get_db():
    """FastAPI Dependency: yields a connection from the pool and safely returns it."""
    with db_pool.connection() as conn:
        yield conn