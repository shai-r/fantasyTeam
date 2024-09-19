import psycopg2
from psycopg2.extras import RealDictCursor
from config.sql_config import SQL_URI

def get_db_connection():
    return psycopg2.connect(SQL_URI, cursor_factory=RealDictCursor)

def create_players_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            api_id VARCHAR(16) NOT NULL,
            player_name VARCHAR(32) NOT NULL
            )
        ''')
    connection.commit()

def create_player_seasons_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS player_seasons (
                id SERIAL PRIMARY KEY,
                player_id INTEGER NOT NULL,
                team VARCHAR(8) NOT NULL,
                position VARCHAR(16) NOT NULL,
                season INTEGER NOT NULL,
                points INTEGER NOT NULL,
                games INTEGER NOT NULL,
                two_percent FLOAT NOT NULL,
                three_percent FLOAT NOT NULL,
                atr FLOAT NOT NULL,
                FOREIGN KEY (player_id) 
                    REFERENCES players(id) 
                        ON DELETE CASCADE
            )
        ''')
    connection.commit()

def create_teams_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS teams (
            id SERIAL PRIMARY KEY,
            team_name VARCHAR(16) NOT NULL,
            season INTEGER
            )
        ''')
    connection.commit()

def create_team_players_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS team_players (
                id SERIAL PRIMARY KEY,
                team_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                position VARCHAR(16) NOT NULL,
                FOREIGN KEY (player_id)
                    REFERENCES player_seasons(id)
                        ON DELETE CASCADE,
                FOREIGN KEY (team_id)
                    REFERENCES teams(id)
                        ON DELETE CASCADE
            )
    ''')
    connection.commit()

def create_all_tables():
    create_players_table()
    create_player_seasons_table()
    create_teams_table()
    create_team_players_table()

def drop_players_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS players")
        connection.commit()

def drop_player_seasons_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS player_seasons")
        connection.commit()


def drop_teams_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS teams")
        connection.commit()

def drop_team_players_table():
    with get_db_connection() as connection, connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS players_table")
        connection.commit()

def drop_all_tables():
    drop_team_players_table()
    drop_teams_table()
    drop_player_seasons_table()
    drop_players_table()