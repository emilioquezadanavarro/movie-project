from sqlalchemy import create_engine, text, Select

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=False)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL
        )
    """))
    connection.commit()

def get_movies():
    """

    Load the whole movies database from the SQL table and return it
    in the old dictionary format.

    """
    with engine.connect() as connection:
        query = text('SELECT title, year, rating FROM movies')
        result = connection.execute(query)
        all_rows = result.fetchall()

        all_movies_dict = {} # Create an empty dictionary to store the formatted data

        # Loop through each row
        for row in all_rows:

            # Convert the row to the old dictionary format

            all_movies_dict[row.title] = {
                "year": row.year,
                "rating": row.rating
            }
        return all_movies_dict

def add_movie(title: str, year: int, rating: float):

    """ Add a movie to the database. """

    with engine.connect() as connection:

        # Define the query avoiding SQL injection
        query = text('INSERT INTO movies (title, year, rating) VALUES (:title, :year, :rating)')

        connection.execute(query, {
            "title": title,
            "year": year,
            "rating": rating
        })
        connection.commit() # Save the changes

