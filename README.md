# 🍿 My Movies Database (CLI Application)

This is a command-line application designed to manage a personal movie collection. It fetches movie details from the OMDb API, stores the collection in a local SQLite database, and allows for various operations including adding, deleting, updating, and generating a static web gallery of your movies.

## ✨ Key Features

* **API Integration:** Fetches real-time movie data (Year, Rating, Poster URL) from the OMDb API.
* **Persistent Storage:** Stores movie data in a local SQLite database (`data/movies.db`) using the SQLAlchemy core library.
* **Security Best Practice:** Uses environment variables (`python-dotenv`) to securely manage the OMDb API key.
* **Efficiency:** Functions (add, delete, update) are refactored to perform targeted database queries (single SELECT/DELETE/UPDATE hits) instead of inefficiently loading the entire database into memory.
* **Functionality:** Supports detailed statistics (Average, Median, Best/Worst movies), search, sorting, and random selection.
* **Static Site Generation:** Creates a static `index.html` file using your collected movie data, ready for local viewing or external hosting.

## 🛠️ Setup and Installation

### 1. Prerequisites

Ensure you have Python 3.8+ installed.

### 2. Installation

1.  **Clone the Repository:**
    ```bash
    git clone git@github.com:emilioquezadanavarro/movie-project.git
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### 3. API Key Configuration

The application requires an API key from OMDb.

1.  **Create `.env` file:** In the root of your project directory, create a file named `.env`.
2.  **Add Key:** Add your API key using the following format:
    ```text
    OMDB_API_KEY="YOUR_ACTUAL_OMDB_API_KEY_HERE"
    ```
    *Note: The `.env` file is in your `.gitignore` and should never be committed to a public repository.*

### 4. Database Initialization

The application will automatically create the `data/movies.db` file and initialize the `movies` table schema when run for the first time.

### 5. Running the Application

```bash
python movies.py
```

## 🚀 Usage

Main Menu Options

0. Exit - Closes the application.
1. List movies - Displays all movies by title, rating, and year.
2. Add movie - Searches OMDb for movie title and adds it to the database.
3. Delete movie - Removes a movie by title.
4. Update movie - Updates the rating for an existing movie.
5. Stats - Shows average, median, best, and worst-rated movies.
6. Random movie - Selects a random movie from database
7. Search movie - Searches for movies by title substring.
8. Movie sorted by rating - List of movies sorted by rating
9. Generate website - Creates a static index.html file in the root directory.

## 💡 Development and Debugging

The application is configured to assist with development:

Database Debugging: The SQLAlchemy engine is set with echo=True in movie_storage_sql.py, which prints every generated SQL query and its parameters to the console. This is invaluable for debugging database interactions.

## 📄 License

This project is open-source and available for educational purposes.

## 🤝 Contributing

Feel free to fork this repository and submit pull requests for any improvements!

